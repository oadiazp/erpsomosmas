from datetime import datetime

import pytest
from mixer.backend.django import mixer

from apps.core.services import ExpensesGetter

pytestmark = pytest.mark.django_db


class TestExpensesGetter:
    def test_getter(self):
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 1, 1),
                    income=True)
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 1, 2),
                    income=True)
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 1, 3),
                    income=True)
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 2, 1),
                    income=False)
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 2, 1),
                    income=False)

        assert ExpensesGetter.get(
            start=datetime(2020, 1, 1),
            end=datetime(2020, 2, 28)
        ).count() == 2

        assert ExpensesGetter.total(
            start=datetime(2020, 1, 1),
            end=datetime(2020, 2, 28)
        ) == 200
