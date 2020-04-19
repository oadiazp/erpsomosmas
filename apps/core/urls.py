from django.urls import path

from apps.core.views import ProfileUpdateView

urlpatterns = [
    path('profile/', ProfileUpdateView.as_view(), name='accounts_profile'),
]
