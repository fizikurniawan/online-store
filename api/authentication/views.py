from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer


class RegisterViewSet(GenericViewSet):
    '''
    Register user (auto verified/active)

    ## Register user
    '''
    serializer_class = RegisterSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # create user
        password = serializer.validated_data.get('password')
        user = User.objects.create(**serializer.validated_data)
        user.set_password(password)
        user.save()

        return Response({'status': 'success', 'message': 'success register'})


class LoginViewSet(GenericViewSet):
    '''
    Login user

    ## Login User

    using username and password
    '''

    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # return token
        user = serializer.validated_data.get('user')
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'status': 'success',
            'message': 'Logged!',
            'token': token.key
        })
