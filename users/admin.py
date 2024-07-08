from django.contrib import admin
from .models import ExtendUser

# Register your models here.
admin.site.register(ExtendUser)

# app = apps.get_app_config('graphql_auth')