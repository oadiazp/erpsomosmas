from django.views.generic import TemplateView

from apps.reports.services import FinancesGeneral


class FinancesAllView(TemplateView):
    template_name = 'reports/general.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incomes'] = FinancesGeneral.incomes()
        context['expenses'] = FinancesGeneral.expenses()

        return context


