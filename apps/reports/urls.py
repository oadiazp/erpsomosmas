from django.urls import path

from apps.reports.views import FinancesAllView, MembersView, ContinentsView

urlpatterns = [
    path(
        'finances/general',
        FinancesAllView.as_view(),
        name='report_general_finances'
    ),
    path(
        'members/',
        MembersView.as_view(),
        name='report_members'
    ),
    path(
        'json/continents',
        ContinentsView.as_view(),
        name='json_continents'
    ),
]
