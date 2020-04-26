import pytest
from mixer.backend.django import mixer

from apps.reports.services import FinancesGeneral

pytestmark = pytest.mark.django_db


class TestFinancesGeneral:
    def test_incomes(self):
        mixer.blend('core.Payment', amount=10)
        mixer.blend('core.Payment', amount=30)
        mixer.blend('core.Payment', amount=150)
        mixer.blend('core.Setting', key='LAST_CONSOLIDATED_INCOME', value=1000)

        assert FinancesGeneral.incomes() == 1190.0

    def test_expenses(self):
        mixer.blend('core.Expense', amount=10)
        mixer.blend('core.Expense', amount=30)
        mixer.blend('core.Expense', amount=150)
        mixer.blend('core.Setting', key='LAST_CONSOLIDATED_EXPENSE', value=1000)

        assert FinancesGeneral.expenses() == 1190.0

    def test_expenses_only_consolidated(self):
        mixer.blend('core.Setting', key='LAST_CONSOLIDATED_EXPENSE', value=1000)

        assert FinancesGeneral.expenses() == 1000.0

    def test_fixed_expenses(self):
        assert FinancesGeneral.fixed_expenses() == 0.0
