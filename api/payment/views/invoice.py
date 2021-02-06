from libs.viewsets import ListAndRetrieveViewSet
from django.shortcuts import Http404
from django.http import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework import status

from api.payment.models import Invoice, InvoiceItem
from api.product.models import Product
from api.payment.serializers.read import InvoiceReadSerializer, InvoiceDetailReadSerializer
from api.payment.serializers.write import PayInvoiceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class InvoiceViewSet(ListAndRetrieveViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Invoice.objects.filter(
        deleted_at__isnull=True
    )

    def get_serializer_class(self):
        serializer_class = InvoiceReadSerializer
        if self.action == 'retrieve':
            serializer_class = InvoiceDetailReadSerializer
        elif self.action == 'pay_invoice':
            serializer_class = PayInvoiceSerializer

        return serializer_class

    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(
            user=request.user
        )

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()

        if instance.user != user:
            raise Http404

        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='pay', serializer_class=PayInvoiceSerializer)
    def pay_invoice(self, request, uuid=None):
        instance = self.get_object()
        if instance.user != request.user:
            raise Http404

        if instance.status == 'success':
            return Response({
                'status': 'error',
                'message': 'Invoice has already paid.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # check stock is available
        inv_items = InvoiceItem.objects.filter(
            invoice=instance, deleted_at__isnull=True)
        product_unavailable = []
        for item in inv_items:
            product_object = Product.objects.get(uuid=product.uuid)
            if product_object.stock < item.qty:
                product_unavailable.append({
                    'uuid': product_object.uuid,
                    'current_stock': product_object.stock
                })

        # error if product unavailable
        if product_unavailable:
            return Response({
                'status': 'error',
                'message': 'Some product stock non available',
                'data': product_unavailable
            }, status=status.HTTP_400_BAD_REQUEST)

        # response list payment method

        return Response({
            'status': 'success',
            'message': 'Success generate transaction',
            'data': {
                'bank_number': '111-111-111-111',
                'bank_name': 'Bank Jago',
                'owner': 'PT. Online Shop'
            }
        })
