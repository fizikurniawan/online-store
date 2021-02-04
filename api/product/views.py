from libs.viewsets import ListAndRetrieveViewSet

from api.product.models import Category
from .serializers.read.category import CategoryReadSerializer


class CategoryViewSet(ListAndRetrieveViewSet):

    queryset = Category.objects.filter(deleted_at__isnull=True)

    def get_serializer_class(self):
        action = self.action
        if action == 'list' or 'retrieve':
            serializer_class = CategoryReadSerializer
        elif action == 'create':
            pass

        return serializer_class
