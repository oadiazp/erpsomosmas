from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView, RedirectView, DetailView

from apps.core.forms import ProfileUpdateForm, ProfilePaymentMethod
from apps.core.models import Profile, Payment
from apps.core.payment_methods import PayPalPaymentMethod
from apps.core.services import ReceivePayment


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
        context['paypal_plan'] = self.object.paypal_plan if self.object.country else ''
        context['client_id'] = settings.PAYPAL_CLIENT_ID
        context['price'] = self.object.membership_price if self.object.country else ''

        return context


class WebhookView(View):
    def post(self, request):
        service = ReceivePayment(request.body.decode('utf-8'))
        service.execute(
            settings.PAYPAL_MODE,
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_CLIENT_SECRET
        )

        return HttpResponse()


class SetPayPalEmailView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        profile = Profile.objects.filter(user__id=self.request.user.id).first()
        profile.paypal_email = self.request.GET.get('email', None)
        profile.save()

        profile.add_payment(
            profile.membership_price,
            self.request.GET.get('order_id')
        )

        return reverse('accounts_general_profile')


class ProfileDetailView(ProfileUpdateView):
    def get_template_names(self):
        return [
            'core/profile_detail.html'
        ]

    def get_form_class(self):
        return ProfileUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.filter(profile=self.object)

        return context

    def get_object(self, queryset=None):
        return Profile.objects.filter(user__id=self.request.user.id).first()

    def get_success_url(self):
        return reverse('accounts_general_profile')


class RedirectMainView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            return reverse('accounts_general_profile')

        return reverse('auth_login')
