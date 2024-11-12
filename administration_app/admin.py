from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Permissions, PermissionApp, CustomGroup, User

User = get_user_model()


class PermissionsAdmin(admin.ModelAdmin):
    list_display = ("permission_app", "name", "codename")


# the original UserAdmin
admin.site.register(User)

# Register the new CustomUserAdmin
admin.site.register(CustomGroup)
# admin.site.register(User, CustomUserAdmin)
admin.site.register(PermissionApp)
admin.site.register(Permissions, PermissionsAdmin)
