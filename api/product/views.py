from rest_framework import status
from rest_framework.viewsets import mixins
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from slugify import slugify

from libs.viewsets import ListAndRetrieveViewSet
from libs.permission import IsAuthenticatedOrReadOnly
from api.product.models import Category, Product, ProductMedia

from .serializers.read.category import CategoryReadSerializer, CategoryDetailReadSerializer
from .serializers.read.product import ProductReadSerializer
from .serializers.write.category import CategoryWriteSerializer
from .serializers.write.product import ProductWriteSerializer


class CategoryViewSet(ListAndRetrieveViewSet, mixins.CreateModelMixin):

    queryset = Category.objects.filter(deleted_at__isnull=True)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, )

    def get_serializer_class(self):
        action = self.action
        if action == 'list':
            serializer_class = CategoryReadSerializer
        elif action == 'retrieve':
            serializer_class = CategoryDetailReadSerializer
        elif action == 'create':
            serializer_class = CategoryWriteSerializer

        return serializer_class

    def list(self, request, *args, **kwargs):
        search = self.request.query_params.get('search')
        if search:
            queryset = self.get_queryset().filter(
                display_name__icontains=search
            )
            self.queryset = queryset

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()

        product_queryset = Product.objects.filter(
            category=instance,
            deleted_at__isnull=True
        )

        page = self.paginate_queryset(product_queryset)

        if page:
            product_serializer = ProductReadSerializer(
                page,
                many=True
            )
            product_serializer = self.get_paginated_response(
                product_serializer.data)
        else:
            product_serializer = ProductReadSerializer(
                product_queryset,
                many=True
            )

        serializer = serializer_class(instance, context={
            'product_serializer': product_serializer})

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        file_instance = serializer.validated_data.get('file')
        display_name = serializer.validated_data.get('display_name')

        # get or create existing category
        category_instance = Category.objects.filter(
            display_name=display_name,
            deleted_at__isnull=True
        ).last()

        if not category_instance:
            category_instance = Category.objects.create(
                display_name=display_name,
                short_name=slugify(display_name),
                thumbnail=file_instance
            )
        else:
            category_instance.short_name = slugify(display_name)
            category_instance.thumbnail = file_instance
            category_instance.save()

        return Response({
            'status': 'success',
            'message': 'Success create category'
        }, status=status.HTTP_201_CREATED)


class ProductViewSet(ListAndRetrieveViewSet, mixins.CreateModelMixin):
    queryset = Product.objects.filter(
        deleted_at__isnull=True
    )
    filter_backends = (SearchFilter, )

    def get_serializer_class(self):
        action = self.action
        if action == 'list' or action == 'retrieve':
            serializer_class = ProductReadSerializer
        else:
            serializer_class = ProductWriteSerializer
        return serializer_class

    def list(self, request, *args, **kwargs):
        # search product by name
        search = self.request.query_params.get('search')
        if search:
            queryset = self.get_queryset().filter(
                display_name__icontains=search
            )
            self.queryset = queryset

        return super().list(request, *args, **kwargs)

    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_medias = serializer.validated_data.pop('media')
        product, _ = Product.objects.get_or_create(**serializer.validated_data)

        # create product media
        for media in product_medias:
            ProductMedia.objects.create(
                product=product,
                **media
            )

        return Response({
            'status': 'success',
            'message': 'success create product'
        }, status=status.HTTP_201_CREATED)
