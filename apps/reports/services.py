from django.db.models import Sum
from geonamescache import GeonamesCache

from apps.core.models import Setting, Payment, Expense, Donation, Profile


class Members:
    @staticmethod
    def amount():
        return Profile.objects.count()

    @staticmethod
    def grouped_by_continents():
        gc = GeonamesCache()

        return [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [
                        [data['bbox']['e']]
                    ]
                }
            } for continent, data in gc.get_continents().items()
        ]
        {k: v['bbox'] for k, v in gc.get_continents().items()}


class FinancesGeneral:
    @staticmethod
    def incomes():
        incomes = FinancesGeneral.memberships()
        donations = FinancesGeneral.donations()
        consolidated = float(Setting.get('LAST_CONSOLIDATED_INCOME'))

        sources = [
            incomes,
            donations,
            consolidated
        ]

        return sum([source for source in sources if source is not None])

    @staticmethod
    def donations():
        donations = Donation.objects.all().aggregate(
            Sum('amount')
        )['amount__sum']

        return donations if donations else 0.0

    @staticmethod
    def memberships():
        incomes = Payment.objects.all().aggregate(Sum('amount'))['amount__sum']

        return incomes if incomes else 0.0

    @staticmethod
    def expenses():
        expenses = Expense.objects.all().aggregate(Sum('amount'))['amount__sum']
        consolidated = float(Setting.get('LAST_CONSOLIDATED_EXPENSE'))

        sources = [
            expenses,
            consolidated
        ]

        return sum([source for source in sources if source is not None])

    @staticmethod
    def fixed_expenses():
        fixed = Expense.objects.filter(
            fixed=True
        ).aggregate(Sum('amount'))['amount__sum']

        return fixed if fixed else 0.0

    @staticmethod
    def variable_expenses():
        variable = Expense.objects.filter(
            fixed=False
        ).aggregate(Sum('amount'))['amount__sum']

        if variable:
            return variable

        return variable if variable else 0.0
