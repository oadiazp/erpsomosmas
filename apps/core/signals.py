from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.emails import WelcomeToClubEmail, NewClubMemberEmail
from apps.core.models import Profile
from apps.core.services import BestClubMatcher


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def find_best_club(sender, created, instance, **kwargs):
    best_club = BestClubMatcher.find(instance)

    if best_club is None:
        return

    if best_club == instance.club:
        return

    best_club.members.add(instance)
    welcome_to_club_email = WelcomeToClubEmail(
        destinations=[instance.user.email],
        context={
            'club': best_club,
        }
    )
    welcome_to_club_email.send()

    new_member_email = NewClubMemberEmail(
        destinations=[best_club.coordinator_email],
        context={
            'profile': instance
        }
    )
    new_member_email.send()
