from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyCustomUser

class MyCustomUserAdmin(UserAdmin):
    model = MyCustomUser
    list_display = ("email", "is_staff", "is_active", "is_superuser")  # Alterado de is_admin para is_superuser
    list_filter = ("is_staff", "is_active", "is_superuser")  # Alterado de is_admin para is_superuser
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser")}),  # Alterado de is_admin para is_superuser
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email",)
    filter_horizontal = ()

admin.site.register(MyCustomUser, MyCustomUserAdmin)
