from rest_framework import serializers
from api.product.models import Product


class FlashSaleSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()
    stock = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=20, decimal_places=2)

    def validate(self, data):
        # validate product exists
        product_uuid = data.get('product_uuid')
        stock = data.get('stock')
        try:
            product = Product.objects.get(
                deleted_at__isnull=True,
                uuid=product_uuid
            )
        except Product.DoesNotExist:
            raise serializers.ValidationError({
                'product_uuid': f'uuid {product_uuid} not found'
            })

        # validate stock
        if stock > product.stock_available:
            raise serializers.ValidationError({
                'stock': f'Stock is not enough. available stock {product.stock_available}'
            })

        return data


class RegisterFlashSaleProductSerializer(serializers.Serializer):
    event_name = serializers.CharField()
    start_event = serializers.DateTimeField()
    end_event = serializers.DateTimeField()
    products = FlashSaleSerializer(many=True)
