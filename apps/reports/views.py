from json import loads
from os.path import join

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from apps.reports.services import FinancesGeneral, Members


class FinancesAllView(TemplateView):
    template_name = 'reports/general.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incomes'] = FinancesGeneral.incomes()
        context['expenses'] = FinancesGeneral.expenses()
        context['memberships'] = FinancesGeneral.memberships()
        context['donations'] = FinancesGeneral.donations()
        context['fixed'] = FinancesGeneral.fixed_expenses()
        context['variables'] = FinancesGeneral.variable_expenses()

        return context


class MembersView(TemplateView):
    template_name = 'reports/members.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amount'] = Members.amount()

        return context


class ContinentsView(View):
    def get(self, request):
        return JsonResponse(
            {
                'amount': Members.get_members_amount_by_continent(
                    request.GET.get('name')
                )
            }
        )


class GeoCountriesView(View):
    def get(self, request):
        path = join(settings.BASE_DIR, 'countries.geo.json')
        with open(path, 'r') as f:
            return JsonResponse(loads(f.read()))


class CountriesView(View):
    def get(self, request):
        return JsonResponse(
            {
                'amount': Members.get_members_amount_by_country(
                    request.GET.get('iso3')
                )
            }
        )
