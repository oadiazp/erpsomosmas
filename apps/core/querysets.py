from django.db.models import QuerySet, Q


class ProfileQS(QuerySet):
    def members(self):
        return self.filter(Q(payment__isnull=False) | Q(country='CU'))
