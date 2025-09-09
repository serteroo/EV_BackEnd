from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    STATUS = [("ACTIVE", "Active"), ("INACTIVE", "Inactive")]
    status = models.CharField(max_length=10, choices=STATUS, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True) # fecha o la hora de creacion 
    updated_at = models.DateTimeField(auto_now=True) # registra ultima fecha y hora de modificacion
    deleted_at = models.DateTimeField(null=True, blank=True) # marca el registro como eliminado en vez de borrarlo de la bd


    class Meta:
        abstract = True # no crea tabla propia, se hereda


class Organization(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    def __str__(self): return self.name


class Category(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="categories") # devuelve todos los dispositivos asociados a esa organizacion
    name = models.CharField(max_length=100)
    def __str__(self): return self.name #Muestra el objeto como texxxxxxxtoooooooo


class Zone(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="zones")
    name = models.CharField(max_length=100)
    def __str__(self): return self.name


class Device(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="devices")
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="devices")
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="devices")
    max_allowed = models.FloatField(default=100.0)
    def __str__(self): return self.name

    
class Measurement(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="measurements")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="measurements")
    value = models.FloatField()
    measured_at = models.DateTimeField()
    class Meta:
        ordering = ["-measured_at"]  # útil para “últimas 10”
    def __str__(self): return f"{self.device} @ {self.measured_at:%Y-%m-%d %H:%M}"

class Alert(BaseModel):
    SEVERITY = [("CRITICAL", "Grave"), ("HIGH", "Alta"), ("MEDIUM", "Media"),]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="alerts")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="alerts")
    message = models.CharField(max_length=255)
    severity = models.CharField(max_length=10, choices=SEVERITY)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_on"]
    def __str__(self): return f"{self.device} - {self.severity}"


