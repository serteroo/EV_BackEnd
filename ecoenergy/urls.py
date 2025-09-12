from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts_app.urls')),
    path('monitoring/', include('monitoring_app.urls')),
    path('', RedirectView.as_view(pattern_name='monitoring_app:dashboard', permanent=False)),
    path('', include('usuarios.urls')),
]
