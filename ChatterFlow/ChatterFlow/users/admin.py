from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _



class CustomUserAdmin(UserAdmin):
    # Add profile_image to the fieldsets for existing users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'bio', 'image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Add profile_image to the add_fieldsets for new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'bio', 'image'),
        }),
    )
    
    # Optionally, add profile_image to list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# Register your models with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)