from django.urls import path

from apps.reports.views import (
    MembersView,
    ContinentsView,
    GeoCountriesView,
    CountriesView, FinancesView
)

urlpatterns = [
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
    path(
        'json/geocountries',
        GeoCountriesView.as_view(),
        name='json_geocountries'
    ),
    path(
        'json/countries',
        CountriesView.as_view(),
        name='json_countries'
    ),
    path(
        'finances',
        FinancesView.as_view(),
        name='finances'
    ),
    path(
        'finances/success',
        FinancesView.as_view(),
        name='finances_success'
    ),
]
