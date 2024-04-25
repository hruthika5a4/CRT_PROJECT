from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserModel
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("uname", "user_type", "contact", "dept")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("date_joined", "last_login")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "is_superuser", "groups", "user_permissions",
                "uname", "user_type", "contact", "dept",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(UserModel, CustomUserAdmin)

admin.site.register(Topic)
admin.site.register(LessonPlan)
