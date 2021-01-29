from datetime import datetime
from json import loads
from os.path import join

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, FormView

from apps.core.models import Profile
from apps.core.services import IncomesGetter, ExpensesGetter
from apps.reports.forms import FinancesForm
from apps.reports.services import Members


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


class FinancesView(FormView):
    template_name = 'reports/financials.html'
    form_class = FinancesForm

    def get_success_url(self):
        start_date = self.request.POST.get('start_date')
        end_date = self.request.POST.get('end_date')
        reversed = reverse('finances_success')

        return f"{reversed}?start_date={start_date}&end_date={end_date}"

    def get_initial(self):
        default_start_date = datetime(day=1, month=now().month, year=now().year)
        default_start_date = default_start_date.strftime('%Y-%m-%d')
        default_end_date = now()
        default_end_date = default_end_date.strftime('%Y-%m-%d')

        return {
            'start_date': default_start_date,
            'end_date': default_end_date,
        }

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'start_date' in self.request.GET and 'end_date' in self.request.GET:
            context['incomes'] = IncomesGetter.get(
                self.request.GET.get('start_date'),
                self.request.GET.get('end_date'),
            )
            context['expenses'] = ExpensesGetter.get(
                self.request.GET.get('start_date'),
                self.request.GET.get('end_date'),
            )
            context['total_incomes'] = IncomesGetter.total(
                self.request.GET.get('start_date'),
                self.request.GET.get('end_date'),
            )
            context['total_expenses'] = ExpensesGetter.total(
                self.request.GET.get('start_date'),
                self.request.GET.get('end_date'),
            )

        return context
