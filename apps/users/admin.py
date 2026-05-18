from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Role, User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role__name", "is_active")


class UsersBaseAdmin(ModelAdmin, ImportExportModelAdmin, SimpleHistoryAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(Role)
class RoleAdmin(UsersBaseAdmin):
    list_display = [
        "get_name_display",
        "can_manage_catalog",
        "can_manage_arrivals",
        "can_manage_sales",
        "can_view_reports",
    ]
    list_editable = [
        "can_manage_catalog",
        "can_manage_arrivals",
        "can_manage_sales",
        "can_view_reports",
    ]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Роль", {"fields": ("name",)}),
        ("Права доступа", {
            "fields": (
                "can_manage_catalog",
                "can_manage_arrivals",
                "can_manage_sales",
                "can_view_reports",
            )
        }),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(User)
class UserAdmin(UsersBaseAdmin, BaseUserAdmin):
    resource_class = UserResource
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ["email", "get_full_name", "role", "get_is_active", "get_is_staff"]
    list_filter = ["role", "is_active", "is_staff"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личные данные", {"fields": ("first_name", "last_name", "patronymic", "role")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Служебное", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )

    @admin.display(description="Полное имя")
    def get_full_name(self, obj):
        return obj.full_name

    @admin.display(description="Активен", boolean=True)
    def get_is_active(self, obj):
        return obj.is_active

    @admin.display(description="Сотрудник", boolean=True)
    def get_is_staff(self, obj):
        return obj.is_staff