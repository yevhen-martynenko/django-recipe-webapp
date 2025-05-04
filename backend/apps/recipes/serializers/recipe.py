from rest_framework import serializers, exceptions
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


from apps.recipes.models import (
    Recipe,
    RecipeBlock,
    RecipeSpecialBlock,
    RecipeReport,
    Like,
    View,
)


class BaseSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    url = serializers.HyperlinkedIdentityField(
        view_name='recipe-detail',
        lookup_field='slug',
    )
    url_update = serializers.HyperlinkedIdentityField(
        view_name='recipe-update',
        lookup_field='slug',
    )
    url_delete = serializers.HyperlinkedIdentityField(
        view_name='recipe-delete',
        lookup_field='slug',
    )

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return obj.is_liked_by(user)

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


class RecipeSpecialBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeSpecialBlock
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
    special_blocks = RecipeSpecialBlockSerializer(many=True)
    blocks = RecipeBlockSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'url',
            'url_update',
            'url_delete',
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
            'url_update',
            'url_delete',
            'id',
            'author',

            'views_count',
            'likes_count',

            'created_at',
            'updated_at',
            'published_at',
        ]


class RecipeAdminSerializer(BaseSerializer):
    special_blocks = RecipeSpecialBlockSerializer(many=True)
    blocks = RecipeBlockSerializer(many=True)

    url_ban = serializers.HyperlinkedIdentityField(
        view_name='recipe-ban',
        lookup_field='slug',
    )

    class Meta:
        model = Recipe
        fields = [
            'url',
            'url_ban',
            'id',
            'author',

            'title',
            'slug',
            'description',
            'status',
            'final_image',
            'source_url',
            'tags',
            'private',

            'is_banned',
            'is_featured',
            'is_deleted',
            'deleted_at',

            'is_liked',
            'views_count',
            'likes_count',
            'blocks',
            'special_blocks',

            'meta_title',
            'meta_description',

            'created_at',
            'updated_at',
            'published_at',
        ]
        read_only_fields = fields


class RecipeMinimalSerializer(BaseSerializer):
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'url',
            'id',
            'author',

            'title',
            'description',
            'final_image',

            'is_liked',
            'views_count',
            'likes_count',
            
            'published_at',
        ]
        read_only_fields = fields


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

    def _get_macronutrients(self, special_blocks: list[dict]) -> dict:
        """
        Extracts macronutrients from the special blocks if available
        """
        for block in special_blocks:
            if block.get('type') == 'macronutrients':
                content = block.get('content', {})
                return {
                    'calories': content.get('calories'),
                    'protein': content.get('protein'),
                    'fat': content.get('fat'),
                    'carbs': content.get('carbs'),
                }
        return {}

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tags', [])
        blocks = self.context.get('blocks', [])
        special_blocks = self.context.get('special_blocks', [])
        macronutrients = self._get_macronutrients(special_blocks)

        recipe = Recipe.objects.create(
            author=user,
            **validated_data,
            **macronutrients
        )

        recipe.tags.set(tags)
        return recipe


class DeletedRecipeSerializer(RecipeSerializer):
    is_deleted = serializers.BooleanField()

    url_restore = serializers.HyperlinkedIdentityField(
        view_name='recipe-restore',
        lookup_field='slug',
    )

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + [
            'url_restore',
            'is_deleted',
        ]
        read_only_fields = [
            field for field in RecipeSerializer.Meta.fields
            if field != 'is_deleted'
        ] + ['url_restore']


class RecipeBanSerializer(RecipeAdminSerializer):
    is_banned = serializers.BooleanField()

    class Meta:
        model = Recipe
        fields = RecipeAdminSerializer.Meta.fields
        read_only_fields = [
            field for field in RecipeAdminSerializer.Meta.fields
            if field != 'is_banned'
        ]


class RecipeStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',

            'title',
            'description',
            'tags',
            'private',

            'views_count',
            'likes_count',

            'created_at',
            'updated_at',
            'published_at',
        ]
        read_only_fields = fields


class RecipeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeReport
        fields = [
            'id',
            'recipe',

            'user',
            'description',
            'status',

            'created_at',
        ]
        read_only_fields = [
            'id',
            'recipe',

            'user',
            'description',

            'created_at',
        ]
