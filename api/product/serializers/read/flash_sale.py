from rest_framework import serializers

from api.product.models import FlashSale, ProductFlashSale


class ProductFlashSaleSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, instance):
        product_instance = instance.product
        return {
            'uuid': product_instance.uuid,
            'display_name': product_instance.display_name,
            'thumbnail': product_instance.thumbnail.get_url()
            if product_instance.thumbnail and product_instance.thumbnail.file else None
        }

    class Meta:
        model = ProductFlashSale
        fields = ('product', 'stock', 'price')


class FlashSaleReadSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, instance):
        product_qs = ProductFlashSale.objects.filter(
            flash_sale=instance
        )

        serializer = ProductFlashSaleSerializer(product_qs, many=True)
        return serializer.data

    class Meta:
        model = FlashSale
        fields = ('event_name', 'start_event', 'end_event', 'products')
