from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import CustomUser

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ("id", "username", "email", "first_name", "last_name", "author_pseudonym")

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'author_pseudonym')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# Correct way to register the CustomUser model with the UserAdmin class
admin.site.register(CustomUser, UserAdmin)
