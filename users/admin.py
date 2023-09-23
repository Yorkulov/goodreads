from django.contrib import admin

from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
