from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class ComalUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone")

class ComalUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"

@admin.register(User)
class ComalUserAdmin(UserAdmin):
    model = User
    add_form = ComalUserCreationForm
    form = ComalUserChangeForm
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "phone", "is_staff")
    search_fields = ("email", "first_name", "last_name", "phone")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "phone")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "first_name", "last_name", "phone", "password1", "password2", "is_staff", "is_superuser")}),)
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("last_login", "date_joined")
