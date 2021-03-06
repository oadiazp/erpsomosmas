from json import loads

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, RedirectView, TemplateView
from registration.backends.default.views import ResendActivationView

from apps.core.emails import WelcomeEmail, PaymentConfirmationEmail
from apps.core.forms import (
    ProfileUpdateForm,
    CustomResendActivationForm,
    CustomPasswordResetForm, CustomAuthenticationForm
)
from apps.core.models import Profile, Payment, Setting
from apps.core.services import ReceivePayment, PaymentCounter, UserRemoval


class RedirectProfileView(RedirectView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        profile = Profile.objects.filter(user__id=self.request.user.id).first()

        if not profile.is_complete:
            return reverse('accounts_profile')

        if not profile.has_payments or not profile.country == 'CU':
            return reverse('accounts_payment')

        return reverse('accounts_general_profile')


class PaymentView(TemplateView):
    template_name = 'core/profile_select_payment_method.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user__id=request.user.id)

        if not profile:
            return super().dispatch(request, *args, **kwargs)

        profile = profile.last()

        if not profile.has_payments:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseRedirect(
            redirect_to=reverse('accounts_general_profile')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user__id=self.request.user.id)\

        if profile:
            profile = profile.first()

            if profile.country:
                context['paypal_plan'] = profile.paypal_plan
                context['price'] = profile.membership_price
            else:
                context['paypal_plan'] = ''
                context['price'] = ''

        context['client_id'] = settings.PAYPAL_CLIENT_ID

        return context


class ProfileUpdateView(UpdateView):
    template_name = 'core/profile_update.html'
    form_class = ProfileUpdateForm

    def get_success_url(self):
        if self.object.country == 'CU' or self.object.has_payments:
            return reverse_lazy('accounts_general_profile')

        return reverse_lazy('accounts_payment')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Profile.objects.filter(user__id=self.request.user.id).first()

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


class WebhookView(View):
    def post(self, request):
        service = ReceivePayment(loads(request.body.decode('utf-8')))
        service.execute(
            settings.PAYPAL_MODE,
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_CLIENT_SECRET
        )

        if PaymentCounter(email=service.email).amount == 1:
            email = WelcomeEmail(destinations=[service.email])
        else:
            email = PaymentConfirmationEmail(destinations=[service.email])
        email.send()

        return HttpResponse()


class SetPayPalEmailView(RedirectView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        profile = Profile.objects.filter(user__id=self.request.user.id).first()
        profile.paypal_email = self.request.GET.get('email', None)
        profile.save()

        return reverse('accounts_general_profile')


class ProfileDetailView(ProfileUpdateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        if Setting.get('MAINTENANCE_MODE') == '1':
            return reverse('maintenance')

        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            return reverse('accounts_redirect')

        return reverse('auth_login')


class CustomResendActivationView(ResendActivationView):
    form_class = CustomResendActivationForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('auth_password_reset_done')


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm


class ResubscribeView(PaymentView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateView, self).dispatch(request, *args, **kwargs)


class MaintenanceView(TemplateView):
    template_name = 'core/maintenance.html'


class RemoveMembershipView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        UserRemoval.remove_user(self.request.user)

        return reverse('auth_logout')