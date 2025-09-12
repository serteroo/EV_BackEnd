from django.urls import path
from . import views

app_name = 'monitoring_app'  

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("devices/", views.devices_list, name="devices_list"),
    path("devices/<int:pk>/", views.device_detail, name="device_detail"),  
    path("measurements/", views.measurements_list, name="measurements_list"),
    path("alerts/", views.alerts_list, name="alerts_list"),
]  