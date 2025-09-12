from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empresa')
    nombre_empresa = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre_empresa

@receiver(post_save, sender=User)
def crear_empresa(sender, instance, created, **kwargs):
    if created:
        Empresa.objects.create(user=instance, nombre_empresa=instance.username)

@receiver(post_save, sender=User)
def guardar_empresa(sender, instance, **kwargs):
    instance.empresa.save()
