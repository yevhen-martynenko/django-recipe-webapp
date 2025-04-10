from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer, UserProfileSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserProfileSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


user_register_view = UserRegisterView.as_view()
