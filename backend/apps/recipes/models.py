import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)


class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    final_image = models.ImageField(upload_to='static/recipes/', null=True, blank=True)
    source_url = models.URLField(blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)
    private = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0)
    viewed_by = models.ManyToManyField(User, related_name='viewed_recipes', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def add_view(self, user):
        if user.is_authenticated and not self.viewed_by.filter(id=user.id).exists():
            self.viewed_by.add(user)
            self.views += 1
            self.save(update_fields=["views"])

    @property
    def views_count(self):
        return self.views
