from rest_framework import serializers
from api.product.models import Product, Category
from api.common.models import File


class ProductMediaWriteSerializer(serializers.Serializer):
    file_uuid = serializers.CharField()
    order = serializers.IntegerField()

    def validate(self, data):
        file_uuid = data.pop('file_uuid')
        file_exists = File.objects.filter(
            deleted_at__isnull=True,
            uuid=file_uuid
        )

        if not file_exists.exists():
            raise serializers.ValidationError({
                'file_uuid': f'file_uuid {file_uuid} is not found.'
            })

        data['file'] = file_exists.last()
        return data


class ProductWriteSerializer(serializers.ModelSerializer):
    category_uuid = serializers.CharField()
    media = ProductMediaWriteSerializer(many=True)
    file_uuid = serializers.CharField()

    def validate(self, data):
        file_uuid = data.pop('file_uuid')
        category_uuid = data.pop('category_uuid')

        file_exists = File.objects.filter(
            deleted_at__isnull=True,
            uuid=file_uuid
        )

        category = Category.objects.filter(
            deleted_at__isnull=True,
            uuid=category_uuid
        )

        if not file_exists.exists():
            raise serializers.ValidationError({
                'file_uuid': f'file_uuid {file_uuid} is not found.'
            })

        if not category.exists():
            raise serializers.ValidationError({
                'category_uuid': f'category_uuid {category_uuid} is not found.'
            })

        data['thumbnail'] = file_exists.last()
        data['category'] = category.last()
        return data

    class Meta:
        model = Product
        fields = ('category_uuid', 'file_uuid', 'display_name',
                  'price', 'stock', 'is_available', 'description', 'media')
