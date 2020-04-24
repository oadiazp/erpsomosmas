from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.core.views import ProfileUpdateView, WebhookView

urlpatterns = [
    path('profile/', ProfileUpdateView.as_view(), name='accounts_profile'),
    path('webhook/', csrf_exempt(WebhookView.as_view()), name='webhook'),
]
