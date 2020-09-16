from django.core.management import BaseCommand

from apps.core.models import Profile, BestClubMatcher


class Command(BaseCommand):
    def handle(self, *args, **options):
        member: Profile
        for member in Profile.objects.members().filter(club=None):
            club = BestClubMatcher.find(member)
            member.club = club
            member.save()