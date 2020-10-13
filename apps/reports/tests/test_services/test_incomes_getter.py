from datetime import datetime

import pytest
from mixer.backend.django import mixer

from apps.core.services import IncomesGetter

pytestmark = pytest.mark.django_db


class TestIncomesGetter:
    def test_getter(self):
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 1, 1),
                    income=True)
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 1, 2),
                    income=True)
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 1, 3),
                    income=True)
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 2, 1),
                    income=True)
        mixer.blend('reports.Move', amount=100, date=datetime(2020, 2, 1),
                    income=True)

        assert IncomesGetter().get(
            start=datetime(2020, 1, 1),
            end=datetime(2020, 1, 30)
        ).count() == 3

        assert IncomesGetter().total(
            start=datetime(2020, 1, 1),
            end=datetime(2020, 1, 30)
        ).total() == 300
