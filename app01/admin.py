from django.contrib import admin
from .models import *


# class PerConfig(admin.ModelAdmin):
#     list_display = ['title', 'url', 'group']

# admin.site.register(UserGroup)
# admin.site.register(PermissionGroup)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Server)
admin.site.register(UserInfo)
admin.site.register(Service)


