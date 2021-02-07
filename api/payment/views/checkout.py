import random
from uuid import uuid4
from datetime import datetime, timedelta

from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.payment.serializers.write import CheckOutWriteSerializer
from api.payment.models import Cart, Invoice, InvoiceItem


class CheckOutViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = CheckOutWriteSerializer
    permission_classes = (IsAuthenticated, )

    def generate_invoice(self):
        uuid_head = str(uuid4())[:4]
        uuid_tail = str(uuid4())[-4:]

        return f'INV-{uuid_tail}-{uuid_head}'

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        cart_uuids = serializer.validated_data.get('cart_uuids')

        # create invoice with pending status
        one_hour_next = datetime.now() + timedelta(hours=1)
        inv = Invoice.objects.create(
            user=user,
            number=self.generate_invoice(),
            status='created',
            expired_pay=one_hour_next
        )

        # create invoice items
        real_chart_uuids = []
        for cart_uuid in cart_uuids:
            cart_uuid = cart_uuid.get('uuid')
            cart = Cart.objects.get(uuid=cart_uuid)
            item = InvoiceItem.objects.filter(
                invoice=inv,
                product=cart.product,
                user=user
            ).last()

            if item:
                item.qty = cart.qty
                item.price = cart.price
                item.save()
            else:
                item = InvoiceItem.objects.create(
                    invoice=inv,
                    product=cart.product,
                    user=user,
                    price=cart.price,
                    qty=cart.qty
                )

            real_chart_uuids.append(cart_uuid)

        # delete cart after success checkout
        carts = Cart.objects.filter(uuid__in=real_chart_uuids).delete()

        return Response({
            'status': 'success',
            'message': 'success checkout',
            'data': {
                'invoice': {
                    'uuid': inv.uuid,
                    'number': inv.number
                }
            }
        })
