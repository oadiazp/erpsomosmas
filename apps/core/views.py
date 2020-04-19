from django.urls import reverse
from django.views.generic import UpdateView

from apps.core.forms import ProfileUpdateForm
from apps.core.models import Profile


class ProfileUpdateView(UpdateView):
    form_class = ProfileUpdateForm

    def get_template_names(self):
        if not self.object.is_complete:
            return [
                'core/profile_update.html'
            ]

        return [
            'core/profile_select_payment_method.html'
        ]

    def get_object(self, queryset=None):
        return Profile.objects.filter(user=self.request.user).first()

    def get_success_url(self):
        return reverse('accounts_profile')
