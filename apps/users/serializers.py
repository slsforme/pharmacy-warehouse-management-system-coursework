from rest_framework import serializers
from .models import Role, User


class RoleSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source="get_name_display", read_only=True)

    class Meta:
        model = Role
        fields = [
            "uid", "name", "name_display", "description",
            "can_manage_catalog", "can_manage_arrivals",
            "can_manage_sales", "can_view_reports",
            "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    role_name = serializers.CharField(source="role.get_name_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "uid", "email", "first_name", "last_name", "patronymic",
            "full_name", "role", "role_name",
            "is_active", "is_staff",
            "created_at", "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at", "full_name"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "email", "first_name", "last_name",
            "patronymic", "role", "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
