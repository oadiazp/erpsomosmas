from django.urls import path

from apps.reports.views import FinancesAllView, MembersView, ContinentsView, \
    GeoCountriesView, CountriesView

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
]
