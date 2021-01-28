from django.db.models import QuerySet, Q


class ProfileQS(QuerySet):
    def members(self):
        return self.filter(Q(payment__isnull=False) | Q(country='CU'))

    def sympathizers(self):
        return self.filter(payment__isnull=True).exclude(country='CU')