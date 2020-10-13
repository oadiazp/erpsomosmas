from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from apps.core.models import (
    Profile,
    Setting,
    Payment,
    MassMail,
    Criteria, Club
)


class PaymentInline(admin.TabularInline):
    model = Payment


class ClubFilter(SimpleListFilter):
    title = 'Club'
    parameter_name = 'club'

    def lookups(self, request, model_admin):
        clubs = Club.objects.values('id', 'name')

        return [
            (club['id'], club['name']) for club in clubs
        ]

    def queryset(self, request, queryset):
        value = self.value()

        return queryset.filter(club=value)


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
    csv_fields = [
        'user',
        'phone',
        'city',
        'country'
    ]
    inlines = [
        PaymentInline,
    ]
    list_filter = [ClubFilter]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)


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
    pass
