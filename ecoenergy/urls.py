from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('monitoring_app.urls')),  # rutas de dashboard/mediciones/etc.
    path('', include('usuario.urls')),         # rutas de login/registro/reset
]
