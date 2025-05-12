from datetime import timedelta, datetime

from django.utils import timezone
from django.utils.text import slugify
from rest_framework import serializers, exceptions
from django.db.models import Count
from django.db.models.functions import TruncHour, TruncDate, TruncWeek, TruncMonth, TruncYear
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
    url_report = serializers.HyperlinkedIdentityField(
        view_name='recipe-report',
        lookup_field='slug',
    )
    url_like = serializers.HyperlinkedIdentityField(
        view_name='recipe-like',
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
    blocks = RecipeBlockSerializer(many=True, required=False)
    special_blocks = RecipeSpecialBlockSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'url',
            'url_update',
            'url_delete',
            'url_report',
            'url_like',
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
            'url_report',
            'url_like',
            'id',
            'author',

            'views_count',
            'likes_count',

            'created_at',
            'updated_at',
            'published_at',
        ]

    def update(self, instance, validated_data):
        title = validated_data.get('title')
        if title and title != instance.title:
            new_slug = slugify(title)
            base_slug = new_slug
            counter = 1
            while Recipe.objects.filter(slug=new_slug).exclude(id=instance.id).exists():
                new_slug = f'{base_slug}-{counter}'
                counter += 1
            instance.slug = new_slug
        return super().update(instance, validated_data)


class RecipeAdminSerializer(BaseSerializer):
    blocks = RecipeBlockSerializer(many=True, required=False)
    special_blocks = RecipeSpecialBlockSerializer(many=True, required=False)

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


class RecipeRestoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['is_deleted', 'deleted_at']
        read_only_fields = fields


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
    likes_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    time_series_data = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',
            'title',
            'slug',
            'tags',

            'views_count',
            'likes_count',
            'time_series_data',

            'created_at',
            'updated_at',
            'published_at',
        ]
        read_only_fields = fields

    def _get_time_range_dates(self, time_range):
        end_date = timezone.now()

        if time_range == 'day':
            start_date = end_date
        elif time_range == '3days':
            start_date = end_date - timedelta(days=3)
        elif time_range == 'week':
            start_date = end_date - timedelta(days=7)
        elif time_range == 'month':
            start_date = end_date - timedelta(days=30)
        elif time_range == '3months':
            start_date = end_date - timedelta(days=90)
        elif time_range == '6months':
            start_date = end_date - timedelta(days=180)
        elif time_range == 'year':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=7)

        return start_date, end_date

    def _get_trunc_function(self, time_view):
        if time_view == 'hour':
            return TruncHour, 'hour'
        elif time_view == 'day':
            return TruncDate, 'date'
        elif time_view == 'week':
            return TruncWeek, 'week'
        elif time_view == 'month':
            return TruncMonth, 'month'
        elif time_view == 'year':
            return TruncYear, 'year'
        else:
            return TruncDate, 'date'

    def _get_formatted_date(self, date_value, time_view):
        """
        Format dates consistently based on the time view
        """
        if time_view == 'hour':
            return date_value.strftime('%Y-%m-%d %H:00')
        elif time_view == 'day':
            return date_value.strftime('%Y-%m-%d')
        elif time_view == 'week':
            return f"{date_value.strftime('%Y')}-W{date_value.strftime('%V')}"
        elif time_view == 'month':
            return date_value.strftime('%Y-%m')
        elif time_view == 'year':
            return date_value.strftime('%Y')
        else:
            return date_value.strftime('%Y-%m-%d')

    def get_time_series_data(self, obj):
        time_range = self.context['request'].query_params.get('time-range', 'week')
        time_view = self.context['request'].query_params.get('time-view', 'day')

        start_date, end_date = self._get_time_range_dates(time_range)
        trunc_func, date_field = self._get_trunc_function(time_view)

        views_by_date = View.objects.filter(
            recipe=obj,
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).annotate(
            period=trunc_func('timestamp')
        ).values('period').annotate(
            count=Count('id')
        ).order_by('period')

        likes_by_date = Like.objects.filter(
            recipe=obj,
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).annotate(
            period=trunc_func('timestamp')
        ).values('period').annotate(
            count=Count('id')
        ).order_by('period')

        time_series = []

        total_views = sum(entry['views'] for entry in time_series)
        total_likes = sum(entry['likes'] for entry in time_series)

        return {
            'time_range': time_range,
            'time_view': time_view,
            'total_views': total_views,
            'total_likes': total_likes,
            'engagement_rate': round((total_likes / total_views) * 100) if total_views > 0 else 0,
            'data': time_series
        }


class RecipeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeReport
        fields = [
            'id',
            'recipe',

            'user',
            'reason',
            'response',
            'status',

            'created_at',
        ]
        read_only_fields = [
            'id',
            'recipe',

            'user',
            'response',
            'status',

            'created_at',
        ]
