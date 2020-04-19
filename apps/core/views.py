from django.urls import reverse
from django.views.generic import UpdateView

from apps.core.forms import ProfileUpdateForm, ProfilePaymentMethod
from apps.core.models import Profile, PaymentMethod


class ProfileUpdateView(UpdateView):
    def get_template_names(self):
        if not self.object.is_complete:
            return [
                'core/profile_update.html'
            ]

        return [
            'core/profile_select_payment_method.html'
        ]

    def get_object(self, queryset=None):
        return Profile.objects.filter(user__id=self.request.user.id).first()

    def get_success_url(self):
        return reverse('accounts_profile')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        initial = kw['initial']
        initial.update(self.get_user_initial_values())
        initial.update(self.get_profile_initial_values())
        kw['initial'] = initial

        return kw

    def get_user_initial_values(self):
        return {
            'first_name': self.object.user.first_name,
            'last_name': self.object.user.last_name,
            'email': self.object.user.email
        }

    def get_profile_initial_values(self):
        return {
            'phone': self.object.phone,
            'street': self.object.street,
            'house_number': self.object.house_number,
            'zip_code': self.object.zip_code,
            'state': self.object.state,
            'country': self.object.country
        }

    def form_valid(self, form):
        form.save(True)
        return super().form_valid(form)

    def get_form_class(self):
        if not self.object.is_complete:
            return ProfileUpdateForm

        return ProfilePaymentMethod

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_methods'] = PaymentMethod.objects.all()

        return context




