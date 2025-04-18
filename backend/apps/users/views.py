from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserProfileSerializer,
    UserRegisterSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_serializer = UserRegisterSerializer(user, context={'request': request})
        return Response(
            {
                'user': user_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


user_register_view = UserRegisterView.as_view()
