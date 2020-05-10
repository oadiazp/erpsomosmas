from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.core.views import (
    ProfileUpdateView,
    WebhookView,
    ProfileDetailView,
    SetPayPalEmailView,
    PaymentView, RedirectProfileView,
    CustomResendActivationView,
    CustomPasswordResetView,
    CustomLoginView,
)

urlpatterns = [
    path(
        'login/',
        CustomLoginView.as_view(template_name='registration/login.html'),
        name='auth_login'
    ),
    path(
        'password/reset/',
        CustomPasswordResetView.as_view(),
        name='auth_password_reset'
    ),
    path(
        'activate/resend/',
        CustomResendActivationView.as_view(),
        name='registration_resend_activation'
    ),
    path('profile/', RedirectProfileView.as_view(), name='accounts_redirect'),
    path('profile/update', ProfileUpdateView.as_view(),
         name='accounts_profile'),
    path(
        'profile/general',
        ProfileDetailView.as_view(),
        name='accounts_general_profile'
    ),
    path('payment/', PaymentView.as_view(), name='accounts_payment'),
    path('webhook/', csrf_exempt(WebhookView.as_view()), name='webhook'),
    path(
        'set_paypal_email',
        SetPayPalEmailView.as_view(),
        name='set_paypal_email'
    ),
]
