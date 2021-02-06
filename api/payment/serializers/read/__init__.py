from rest_framework import serializers
from django.db.models import Sum

from api.payment.models import Cart, Invoice, InvoiceItem
from api.product.serializers.read.product import ProductLiteSerializer


class CartReadSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, instance):
        serializer = ProductLiteSerializer(instance.product)
        return serializer.data

    class Meta:
        model = Cart
        fields = ('uuid', 'product', 'created_at', 'qty', 'price')


class InvoiceReadSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, instance):
        items = InvoiceItem.objects.filter(
            deleted_at__isnull=True,
            invoice=instance
        )
        total = sum([(i.price * i.qty) for i in items])

        return total

    class Meta:
        model = Invoice
        fields = ('uuid', 'number', 'created_at', 'total_price', 'status')


class ItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_product(self, instance):
        serializer = ProductLiteSerializer(instance.product)
        return serializer.data

    def get_total_price(self, instance):
        return instance.qty * instance.price

    class Meta:
        model = InvoiceItem
        fields = ('product', 'qty', 'price', 'total_price')


class InvoiceDetailReadSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_total_price(self, instance):
        items = InvoiceItem.objects.filter(
            deleted_at__isnull=True,
            invoice=instance
        )
        total = sum([(i.price * i.qty) for i in items])

        return total

    def get_items(self, instance):
        items = InvoiceItem.objects.filter(
            deleted_at__isnull=True,
            invoice=instance
        )
        serializer = ItemSerializer(items, many=True)

        return serializer.data

    class Meta:
        model = Invoice
        fields = ('uuid', 'number', 'created_at',
                  'total_price', 'status', 'items')
