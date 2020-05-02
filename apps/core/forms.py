from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail

from apps.core.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField(label=_('Surname'))
    email = forms.EmailField()

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
        )

    def save(self, commit=True):
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.email = self.cleaned_data['email']
        self.instance.user.save()

        return super().save(commit)


class RegistrationForm(RegistrationFormUniqueEmail):
    captcha = CaptchaField(label=_('Verification code'))
    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_("I have read and agree to the S+'s basis and principals"),
        error_messages={
            'required': _(
                "You must agree to the basis and principals to register"
            )
        }
    )
