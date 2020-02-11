from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import Profile
from users.serializers import ProfileSerializer


class RegisterAPIView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_data = data["user"]
        if not User.objects.filter(username=user_data["email"]).exists():
            user = User.objects.create(
                username=user_data["email"], email=user_data["email"],
                first_name=user_data["first_name"], last_name=user_data["last_name"]
            )
            user.set_password(user_data["password"])
            token = Token.objects.create(user=user)
            profile = Profile.objects.create(user=user, avatar=data["avatar"])
            return Response({
                "token": token.key,
                "username": user.username,
                "profile_id": profile.id,
                "avatar": profile.avatar.url
            }, status=status.HTTP_201_CREATED)
        else:
            return Response("There is already a registered user with this email.",
                            status=status.HTTP_409_CONFLICT)


class LoginAPIView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        profile = Profile.objects.get(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "profile_id": profile.id,
            "avatar": profile.avatar.url
        }, status=status.HTTP_200_OK)
