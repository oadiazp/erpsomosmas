# from captcha.fields import CaptchaField
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible

from django import forms
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.tokens import default_token_generator

from django.utils.translation import gettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail, ResendActivationForm

from apps.core.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(label=_('Surname'), required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = (
            'phone',
            'street',
            'house_number',
            'zip_code',
            'state',
            'country',
            'photo',
            'city',
        )

    def save(self, commit=True):
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.email = self.cleaned_data['email']
        self.instance.user.save()

        return super().save(commit)


class RegistrationForm(RegistrationFormUniqueEmail):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label='')
    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_("I have read and agree to the S+'s basis and principals"),
        error_messages={
            'required': _(
                "You must agree to the basis and principals to register"
            )
        }
    )


class CustomResendActivationForm(ResendActivationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label='')


class CustomPasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label='')

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        super().save(domain_override, subject_template_name,
                     email_template_name, use_https, token_generator,
                     from_email, request, 'registration/password_reset_email.html',
                     extra_email_context)


class CustomAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label='')
