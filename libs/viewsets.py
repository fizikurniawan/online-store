from rest_framework.viewsets import GenericViewSet, mixins


class ListAndRetrieveViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    lookup_field = 'uuid'
