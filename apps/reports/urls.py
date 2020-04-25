from django.urls import path

from apps.reports.views import FinancesAllView

urlpatterns = [
    path(
        'finances/general',
        FinancesAllView.as_view(),
        name='report_general_finances'
    ),
]
