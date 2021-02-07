from django.shortcuts import Http404
from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from libs.viewsets import ListAndRetrieveViewSet

from api.payment.models import Cart
from ..serializers.read import CartReadSerializer
from ..serializers.write import CartWriteSerializer


class CartViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated, ]
    queryset = Cart.objects.filter(
        deleted_at__isnull=True
    )

    def get_serializer_class(self):
        action = self.action
        serializer_class = CartReadSerializer
        if action == 'create':
            serializer_class = CartWriteSerializer

        return serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            user=request.user
        ).order_by('-created_at')

        self.queryset = queryset

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # validate again product qty
        qty = serializer.validated_data.get('qty')
        product = serializer.validated_data.get('product')
        price = serializer.validated_data.get('price')

        if product and product.stock and product.stock < qty:
            return Response({
                'status': 'error',
                'message': f'Qty greather than available stock. Available stock {product.stock}'
            }, status=status.HTTP_400_BAD_REQUEST)

        # increment qty if already exists on cart
        cart = Cart.objects.filter(product=product, user=request.user).last()
        if not cart:
            Cart.objects.create(product=product, qty=qty,
                                user=request.user, price=price)
        else:
            cart.qty += qty
            cart.price = price
            cart.save()

        return Response({
            'status': 'success'
        })

    def destroy(self, request):
        instance = self.get_object()
        if instance.user != request.user:
            raise Http404

        instance.delete()

        return Response({
            'status': 'success',
            'message': 'success deleted checkout'
        }, status=status.HTTP_204_NO_CONTENT)
