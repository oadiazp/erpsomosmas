from django.db.models import Sum

from apps.core.models import Setting, Payment, Expense, Donation


class FinancesGeneral:
    @staticmethod
    def incomes():
        incomes = Payment.objects.all().aggregate(Sum('amount'))['amount__sum']
        donations = Donation.objects.all().aggregate(
            Sum('amount')
        )['amount__sum']
        consolidated = float(Setting.get('LAST_CONSOLIDATED_INCOME'))

        sources = [
            incomes,
            donations,
            consolidated
        ]

        return sum([source for source in sources if source is not None])

    @staticmethod
    def expenses():
        expenses = Expense.objects.all().aggregate(Sum('amount'))['amount__sum']
        consolidated = float(Setting.get('LAST_CONSOLIDATED_EXPENSE'))

        sources = [
            expenses,
            consolidated
        ]

        return sum([source for source in sources if source is not None])
