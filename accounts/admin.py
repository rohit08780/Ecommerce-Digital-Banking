
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'full_name',
        'phone_number',
        'role',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'full_name',
        'phone_number',
    )

    ordering = ('id',)

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('full_name', 'phone_number', 'role'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'full_name', 'phone_number', 'role'),
        }),
    )
