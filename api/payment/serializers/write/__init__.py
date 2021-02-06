from rest_framework import serializers
from django.utils import timezone

from api.payment.models import Cart
from api.product.models import Product, ProductFlashSale
from libs.constant import PAYMENT_METHOD_CHOICES


class CartWriteSerializer(serializers.ModelSerializer):
    product_uuid = serializers.CharField()

    def validate(self, data):
        is_flash_sale = self._context.get('is_flash_sale', False)
        product_uuid = data.pop('product_uuid')
        qty = data.get('qty')

        product_exists = Product.objects.filter(
            deleted_at__isnull=True,
            uuid=product_uuid,
            is_available=True
        ).last()

        if not product_exists:
            raise serializers.ValidationError({
                'product_uuid': 'Product not found'
            })

        # validate qty
        if qty < 1:
            raise serializers.ValidationError({
                'qty': 'Qty must be greather than 0'
            })

        '''
        Check qty by product type (common, flash sale) with new qty + qty exists
        by user action in datetime
        '''
        now = timezone.now()
        flash_sale_product = ProductFlashSale.objects.filter(
            product=product_exists,
            deleted_at__isnull=True,
            flash_sale__start_event__gte=now,
            flash_sale__end_event__lte=now
        ).last()

        # set price by event and total qty
        price = product_exists.price
        if flash_sale_product and flash_sale_product.stock > qty:
            price = flash_sale_product.price

        total_stock = (flash_sale_product.stock if flash_sale_product else 0) + product_exists.stock
        if qty > total_stock:
            raise serializers.ValidationError({
                'qty': f'Qty greather than available stock. Available stock {total_stock}'
            })

        data['product'] = product_exists
        data['price'] = price
        return data

    class Meta:
        model = Cart
        fields = ('product_uuid', 'qty')


class CartLiteSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()

    def validate(self, data):
        cart_uuid = data.get('uuid')
        try:
            cart_instance = Cart.objects.get(
                deleted_at__isnull=True, uuid=cart_uuid)
        except Cart.DoesNotExist:
            raise serializers.ValidationError({
                'uuid': f'{cart_uuid} not found'
            })

        return data


class CheckOutWriteSerializer(serializers.Serializer):
    cart_uuids = CartLiteSerializer(many=True)


class PayInvoiceSerializer(serializers.Serializer):
    payment_method = serializers.CharField()

    def validate(self, data):
        payment_method = data.get('payment_method')
        if payment_method not in [i[0] for i in PAYMENT_METHOD_CHOICES]:
            raise serializers.ValidationError({
                'payment_method': 'Invalid payment method'
            })

        return data
