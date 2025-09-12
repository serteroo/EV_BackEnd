# accounts_app/apps.py
from django.apps import AppConfig

class AccountsAppConfig(AppConfig):           # nombre de la clase
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts_app'                     # nombre del PAQUETE (carpeta), no 'accounts'
