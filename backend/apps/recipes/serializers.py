from rest_framework import serializers, exceptions
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


from apps.recipes.models import (
    Recipe,
    RecipeBlock,
    SpecialRecipeBlock,
    Tag,
    Like,
    View,
)


class BaseSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    url = serializers.HyperlinkedIdentityField(
        view_name='recipe-detail-update-delete',
        lookup_field='id',
    )

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            return False
        return obj.likes.filter(user=user).exists()

    def to_internal_value(self, data):
        """
        Raise validation error if unknown fields are passed (only on full update/create)
        """
        if not self.partial:
            allowed = set(self.fields)
            incoming = set(data)

            unknown_fields = incoming - allowed
            if unknown_fields:
                raise serializers.ValidationError({
                    field: 'This field is not allowed.' for field in unknown_fields
                })

        return super().to_internal_value(data)


class SpecialRecipeBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialRecipeBlock
        fields = [
            'id',
            'recipe',
            'type',
            'content',
            'order',
        ]
        read_only_fields = [
            'id',
            'recipe',
        ]

    def validate(self, data):
        instance = self.instance or self.Meta.model(**data)
        for attr, value in data.items():
            setattr(instance, attr, value)

        try:
            instance.full_clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

        return data


class RecipeBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeBlock
        fields = [
            'id',
            'recipe',
            'type',
            'content',
            'image',
            'order',
        ]
        read_only_fields = [
            'id',
            'recipe',
        ]

    def validate(self, data):
        instance = self.instance or self.Meta.model(**data)
        for attr, value in data.items():
            setattr(instance, attr, value)

        try:
            instance.full_clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

        return data


class RecipeSerializer(BaseSerializer):
    special_blocks = SpecialRecipeBlockSerializer(many=True)
    blocks = RecipeBlockSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'url',
            'id',
            'author',

            'title',
            'description',
            'status',
            'final_image',
            'source_url',
            'tags',
            'private',

            'calories',
            'protein',
            'fat',
            'carbs',

            'is_liked',
            'views_count',
            'likes_count',
            'blocks',
            'special_blocks',

            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'url',
            'id',
            'author',

            'created_at',
            'updated_at',
        ]


class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'status',
            'final_image',
            'source_url',
            'tags',
            'private',
        ]

    def validate_title(self, value):
        if len(value) > 64:
            raise exceptions.ValidationError('Title is too long')
        return value

    def validate_description(self, value):
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)

        return recipe
