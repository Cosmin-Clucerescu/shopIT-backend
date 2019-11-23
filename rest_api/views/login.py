from django.contrib.auth import authenticate, login, models
from rest_framework import generics, serializers, permissions, response, exceptions


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=1, write_only=True)


class Login(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # We keep an if here, because the exception is not a validation exception but an AuthenticationFailed exception
        if serializer.is_valid():
            username = serializer.validated_data.get("email").lower()
            password = serializer.validated_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is None:
                user = models.User.objects.create_user(username, username, password)
            if user is not None and user.is_active:
                login(request, user)
                return response.Response(data=serializer.data)
        raise exceptions.APIException("Invalid user/password")
