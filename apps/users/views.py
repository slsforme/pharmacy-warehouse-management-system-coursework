from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Role, User
from .serializers import RoleSerializer, UserSerializer, UserCreateSerializer


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering = ["name"]


class UserViewSet(ModelViewSet):
    queryset = User.objects.select_related("role").all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["email", "created_at"]
    ordering = ["email"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """Текущий пользователь"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)