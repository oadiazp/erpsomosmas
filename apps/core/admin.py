from django.contrib import admin
from django.http import HttpResponse

from apps.core.models import Profile, Setting, Payment


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
        'country'
    ]
    inlines = [
        PaymentInline,
    ]

    # def export(self, request, queryset):
    #     csv = CSVMaker(queryset)
    #
    #     with open(csv, 'rb') as fh:
    #         response = HttpResponse(
    #             fh.read(),
    #             content_type="application/vnd.ms-excel"
    #         )
    #
    #         response['Content-Disposition'] = 'inline; filename=miembros.csv'
    #         return response


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)
