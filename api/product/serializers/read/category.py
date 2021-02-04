from rest_framework import serializers

from api.product.models import Category

class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('uuid', 'display_name', 'thumbnail', )