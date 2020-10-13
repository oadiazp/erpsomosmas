from geonamescache import GeonamesCache
from geonamescache.mappers import country

from apps.core.models import Profile


class Members:
    @staticmethod
    def amount():
        return Profile.objects.members().count()

    @classmethod
    def get_members_amount_by_continent(cls, continent):
        countries = cls.get_countries_by_continent(continent)
        return Profile.objects.members().filter(
            country__in=countries
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
        return mapper(iso3)
