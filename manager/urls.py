from django.contrib import admin
from django.urls import path, include

from apps.core.views import RedirectMainView

urlpatterns = [
    path('', RedirectMainView.as_view(), name='home'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('reports/', include('apps.reports.urls')),
    path('accounts/', include('apps.core.urls')),
    path('accounts/', include('registration.backends.default.urls')),
]
