from django.contrib import admin

from apps.core.models import Profile, PaymentMethod


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass
