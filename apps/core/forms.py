from django import forms

from apps.core.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    field_order = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'street',
        'house_number',
        'zip_code',
        'state',
        'country',
    ]

    class Meta:
        model = Profile
        fields = (
            'phone',
            'street',
            'house_number',
            'zip_code',
            'state',
            'country'
        )
