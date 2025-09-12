from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_empresa, name='login_empresa'),
    
    path('register/', views.registro_empresa, name='registro_empresa'),

    path('login-old/', views.login_view, name='login'),
    path('registro-old/', views.registro_view, name='registro'),
    
    path('recuperar-contrasena/', views.recuperar_contrasena_view, name='recuperar_contrasena'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]