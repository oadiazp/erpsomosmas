from django.contrib import admin
from django.shortcuts import render

from apps.core.models import (
    Profile,
    Setting,
    Payment,
    Expense,
    ExpenseKind,
    MassMail,
    MassMailCriteria
)


class PaymentInline(admin.TabularInline):
    model = Payment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'user__username',
        'country',
        'user__email',
    ]
    list_display = [
        'user',
        'first_name',
        'last_name',
        'email',
        'city',
        'country'
    ]
    inlines = [
        PaymentInline,
    ]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'kind',
        'amount',
        'fixed',
    )


@admin.register(ExpenseKind)
class ExpenseKindAdmin(admin.ModelAdmin):
    pass


class MassMailCriteriaInline(admin.TabularInline):
    model = MassMailCriteria


@admin.register(MassMail)
class MassMailAdmin(admin.ModelAdmin):
    inlines = [
        MassMailCriteriaInline,
    ]
    list_display = [
        'name',
        'subject',
        'created',
    ]
    actions = [
        'send_mails',
    ]

    def send_mails(self, request, queryset):
        for mass_mail in queryset:
            mass_mail.send_message()
