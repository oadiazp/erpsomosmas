from django.contrib import admin

from apps.core.models import Profile, PaymentMethod, Setting, Payment


class PaymentInline(admin.TabularInline):
    model = Payment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        PaymentInline,
    ]


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)
