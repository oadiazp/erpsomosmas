from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.core.views import (
    ProfileUpdateView,
    WebhookView,
    ProfileDetailView,
    SetPayPalEmailView,
    PaymentView, RedirectProfileView,
)

urlpatterns = [
    path('profile/', RedirectProfileView.as_view(), name='accounts_redirect'),
    path('profile/update', ProfileUpdateView.as_view(), name='accounts_profile'),
    path(
        'profile/general',
        ProfileDetailView.as_view(),
        name='accounts_general_profile'
    ),
    path('payment/', PaymentView.as_view(), name='accounts_payment'),
    path('webhook/', csrf_exempt(WebhookView.as_view()), name='webhook'),
    path('set_paypal_email', SetPayPalEmailView.as_view(), name='payment'),
]
