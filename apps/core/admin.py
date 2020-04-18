from django.contrib import admin

from apps.core.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
