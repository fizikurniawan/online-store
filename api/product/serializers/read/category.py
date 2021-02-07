from rest_framework import serializers

from api.product.models import Category


class CategoryReadSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        if obj.thumbnail and obj.thumbnail.file:
            return obj.thumbnail.get_url()
        return None

    class Meta:
        model = Category
        fields = ('uuid', 'display_name', 'thumbnail', )


class CategoryDetailReadSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    def get_thumbnail(self, instance):
        if instance.thumbnail and instance.thumbnail.file:
            return instance.thumbnail.get_url()
        return None

    def get_products(self, instance):
        return self._context['product_serializer'].data

    class Meta:
        model = Category
        fields = ('uuid', 'display_name', 'thumbnail', 'products')
