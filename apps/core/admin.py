import csv

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse

from apps.core.models import (
    Profile,
    Setting,
    Payment,
    MassMail,
    Criteria, Club
)
from apps.core.services import UserRemoval


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

        if value:
            return queryset.filter(club=value)

        return queryset


class StatusFilter(SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('members', 'Members',),
            ('sympathizer', 'Sympathizers',),
        ]

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset

        if value == 'members':
            return queryset.members()

        return queryset.sympathizers()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'user__first_name',
        'user__last_name',
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
        'first_name',
        'last_name',
        'email',
        'phone',
        'city',
        'country'
    ]
    inlines = [
        PaymentInline,
    ]
    list_filter = [ClubFilter, StatusFilter]
    actions = ('export', 'unsuscribe')

    def unsuscribe(self, request, queryset):
        [UserRemoval.remove(profile.user) for profile in queryset]

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
                'attachment; filename="profiles.csv"'
        )
        writer = csv.writer(response)

        for profile in queryset:
            writer.writerow([
                getattr(profile, field) for field in self.csv_fields
            ])

        return response


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
