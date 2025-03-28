from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from django.utils.translation import gettext_lazy as _

# Register your models with the custom admin class
admin.site.register(CustomUser)

admin.site.register(Profile)
