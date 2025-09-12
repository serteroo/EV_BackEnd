from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'user', 'telefono', 'fecha_registro']
    search_fields = ['nombre_empresa', 'user__username']