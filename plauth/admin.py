from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('uuid',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    list_display = ('uuid', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('uuid', )
    ordering = ('uuid',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('uuid',)