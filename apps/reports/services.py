from django.db.models import Sum
from geonamescache import GeonamesCache
from geonamescache.mappers import country

from apps.core.models import Setting, Payment, Expense, Donation, Profile


class Members:
    @staticmethod
    def amount():
        return Profile.objects.filter(payment__isnull=False).count()

    @classmethod
    def get_members_amount_by_continent(cls, continent):
        countries = cls.get_countries_by_continent(continent)
        return Profile.objects.filter(
            country__in=countries,
            payment__isnull=False
        ).count()

    @classmethod
    def get_countries_by_continent(cls, continent):
        gc = GeonamesCache()
        continent = [
            v for k, v in gc.get_continents().items() if v['toponymName'] == continent
        ][0]

        return continent['cc2'].split(',')

    @classmethod
    def get_members_amount_by_country(cls, iso3):
        iso2 = cls.convert_iso3_to_iso2(iso3)

        return Profile.objects.members().filter(
            country=iso2
        ).count()

    @classmethod
    def convert_iso3_to_iso2(cls, iso3):
        mapper = country(from_key='iso3', to_key='iso')
        iso2 = mapper(iso3)
        return iso2


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
