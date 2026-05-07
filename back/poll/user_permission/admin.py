from django.contrib import admin

from generic.admin import CustomModelAdmin

from .models import PermissionAction, PermissionType, UserPermission

admin.site.register(PermissionType, CustomModelAdmin(PermissionType))
admin.site.register(PermissionAction, CustomModelAdmin(PermissionAction))
admin.site.register(UserPermission, CustomModelAdmin(UserPermission))
