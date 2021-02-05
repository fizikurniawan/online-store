from rest_framework import serializers

from api.product.models import Product, ProductMedia


class MediaReadSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, instance):
        if instance.file and instance.file.file:
            return instance.file.file.url
        return None

    class Meta:
        model = ProductMedia
        fields = ('order', 'url')


class ProductReadSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_media(self, instance):
        media_queryset = ProductMedia.objects.filter(
            product=instance,
            deleted_at__isnull=True
        ).order_by('order')

        media_serializer = MediaReadSerializer(media_queryset, many=True)

        return media_serializer.data

    def get_thumbnail(self, instance):
        if instance.thumbnail and instance.thumbnail.file:
            return instance.thumbnail.file.url
        return None

    class Meta:
        model = Product
        fields = ('uuid', 'display_name', 'thumbnail', 'media')
