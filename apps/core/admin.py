from django.contrib import admin

from apps.core.models import (
    Profile,
    Setting,
    Payment,
    Expense,
    ExpenseKind,
    MassMail,
    Criteria, Club
)
from apps.core.services import BestClubMatcher


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
    model = Criteria


@admin.register(MassMail)
class MassMailAdmin(admin.ModelAdmin):
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


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    actions = (
        'find_best_matches_to_all_members',
    )

    def find_best_matches_to_all_members(self):
        member: Profile
        for member in Profile.objects.members():
            BestClubMatcher.find(member)
