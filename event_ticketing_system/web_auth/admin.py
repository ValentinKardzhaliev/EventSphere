from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import EventAppUser


class EventAppUserAdmin(auth_admin.UserAdmin):
    list_display = ('username', 'email', 'balance')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'profile_picture', 'balance')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'profile_picture', 'balance'),
        }),
    )


admin.site.register(EventAppUser, EventAppUserAdmin)
