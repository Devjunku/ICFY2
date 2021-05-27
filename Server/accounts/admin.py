from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserCustomAdmin(UserAdmin):
    list_display = ('id', 'username', 'is_superuser',)


admin.site.register(User, UserCustomAdmin)
