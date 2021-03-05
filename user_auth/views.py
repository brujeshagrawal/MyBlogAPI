from django.contrib.auth import get_user_model

from rest_framework import generics, serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK

from .serializers import RegisterSerializer

# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """
        check authentication of users & generate a token
        """

        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
        except serializers.ValidationError as e:
            print(e)
            return Response({
                'error' : 'Try login again.'
            })


        return Response({
            'token': token.key,
        })


class LogoutView(generics.DestroyAPIView):
    """
        class for logging out user
        """
    permission_classes = (IsAuthenticated,)
    model = Token

    def delete(self, request):
        """
        delete token upon logout
        """
        user = request.user
        Token.objects.filter(user=user).delete()

        return Response(
            {'message': 'User logged out successfully.,'},
            status=HTTP_200_OK
        )