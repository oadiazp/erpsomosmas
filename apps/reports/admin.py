from django.contrib import admin

from apps.reports.models import Move


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('concept', 'date', 'amount', 'income')
