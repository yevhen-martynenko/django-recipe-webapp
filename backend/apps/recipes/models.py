import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug'], name='tag_id_slug_idx'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

            base_slug = self.slug
            counter = 1
            while Tag.objects.filter(slug=self.slug).exists():
                self.slug = f'{base_slug}-{counter}'
                counter += 1

        super().save(*args, **kwargs)


class RecipeStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    PENDING = 'pending', 'Pending Moderation'


class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=64, choices=RecipeStatus.choices, default=RecipeStatus.DRAFT)
    final_image = models.ImageField(upload_to='static/recipes/', null=True, blank=True)
    source_url = models.URLField(blank=True, null=True)

    # Nutrition information
    calories = models.PositiveIntegerField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)

    # Relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)

    # Meta
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    private = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)

    # Status
    is_featured = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Statistics
    views = models.PositiveIntegerField(default=0)
    viewed_by = models.ManyToManyField(User, related_name='viewed_recipes', blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # SEO
    meta_title = models.CharField(max_length=64, blank=True)
    meta_description = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug'], name='recipe_id_slug_idx'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

            base_slug = self.slug
            counter = 1
            while Recipe.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def is_ready_for_permanent_deletion(self):
        """
        Returns True if the recipe was soft-deleted more than 7 days ago
        """
        if not self.is_deleted or not self.deleted_at:
            return False
        return timezone.now() >= self.scheduled_permanent_deletion_time()

    def add_view(self, user):
        if user.is_authenticated and not self.viewed_by.filter(id=user.id).exists():
            self.viewed_by.add(user)
            self.views += 1
            self.save(update_fields=["views"])

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def views_count(self):
        return self.views


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_recipes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')
        indexes = [
            models.Index(fields=['created_at']),
        ]
