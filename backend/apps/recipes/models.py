import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=256, unique=True, blank=True, null=True)

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
    slug = models.SlugField(max_length=256, unique=True, blank=True, null=True)
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

    # Status
    private = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

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

    def toggle_like(self, user):
        if not user.is_authenticated:
            return None

        like, created = Like.objects.get_or_create(user=user, recipe=self)
        if not created:
            like.delete()
            return False
        return True

    @property
    def likes_count(self):
        return self.likes.count()

    def add_view(self, user):
        if not user.is_authenticated:
            return
        View.objects.get_or_create(recipe=self, user=user)

    @property
    def views_count(self):
        return self.views.count()


class SpecialRecipeBlock(models.Model):
    INGREDIENTS = 'ingredients'
    TIMES = 'times'
    CALORIES = 'calories'
    MACRONUTRIENTS = 'macronutrients'
    
    BLOCK_TYPE_CHOICES = [
        (INGREDIENTS, 'Ingredients List'),
        (TIMES, 'Preparation & Cooking Time'),
        (CALORIES, 'Calorie Count'),
        (MACRONUTRIENTS, 'Protein, Carbs & Fat Breakdown'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='special_blocks')
    type = models.CharField(max_length=32, choices=BLOCK_TYPE_CHOICES, unique=True)
    content = models.JSONField(
        null=True,
        blank=True,
        help_text="""
            Structured content varies by block type:
            -    Ingredients: {'items': ['flour', 'sugar', 'milk']}
            -    Time: {'prep_minutes': 10, 'cook_minutes': 30}
            -    Calories: {'kcal': 200}
            -    Macronutrients: {'protein': 5, 'carbs': 20, 'fat': 10}
        """.strip()
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = ('recipe', 'type')
        verbose_name = "Special Recipe Block"
        verbose_name_plural = "Special Recipe Blocks"

    def __str__(self):
        return f"{self.recipe.title} - {self.type}"


class RecipeBlock(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    BLOCK_TYPE_CHOICES = [
        (TEXT, 'Text Block'),
        (IMAGE, 'Image Block'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='blocks')
    type = models.CharField(max_length=8, choices=BLOCK_TYPE_CHOICES, default=TEXT)
    content = models.TextField(
        blank=True,
        null=True,
        help_text="""
            Used for TEXT blocks. Example:
            -    'Preheat oven to 350°F (175°C).'
        """.strip()
    )
    image = models.ImageField(
        upload_to='static/recipes/blocks/',
        blank=True,
        null=True,
        help_text="Used for IMAGE blocks."
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Recipe Block'
        verbose_name_plural = 'Recipe Blocks'

    def __str__(self):
        return f"{self.recipe.title} - {self.type}"


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_recipes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')
        indexes = [
            models.Index(fields=['recipe', 'timestamp']),
        ]


class View(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_recipes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')
        indexes = [
            models.Index(fields=['recipe', 'timestamp']),
        ]
