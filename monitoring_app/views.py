from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required  # ← Agrega esta importación
from .models import Organization, Category, Zone, Device, Measurement, Alert

@login_required  # ← Agrega este decorador
def dashboard(request):
    organizations = Organization.objects.all()
    categories = Category.objects.all()
    zones = Zone.objects.all()
    devices = Device.objects.all()
    measurements = Measurement.objects.all()[:10]  # Últimas 10 mediciones
    alerts = Alert.objects.filter(status="ACTIVE")  # Solo alertas activas

    context = {
        "organizations": organizations,
        "categories": categories,
        "zones": zones,
        "devices": devices,
        "measurements": measurements,
        "alerts": alerts,
    }
    return render(request, "monitoring/dashboard.html", context)


def devices_list(request):
    category_id = request.GET.get("category")
    zone_id = request.GET.get("zone")

    devices = Device.objects.all()
    if category_id and category_id != "all":
        devices = devices.filter(category_id=category_id)
    if zone_id and zone_id != "all":
        devices = devices.filter(zone_id=zone_id)

    context = {
        "devices": devices,
        "categories": Category.objects.all(),
        "zones": Zone.objects.all(),
    }
    return render(request, "monitoring/devices_list.html", context)


def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    measurements = device.measurements.all().order_by("-measured_at")[:10]
    alerts = device.alerts.all().order_by("-created_on")[:5]

    context = {
        "device": device,
        "measurements": measurements,
        "alerts": alerts,
    }
    return render(request, "monitoring/device_detail.html", context)


def measurements_list(request):
    measurements = Measurement.objects.order_by("-measured_at")
    return render(request, "monitoring/measurements_list.html", {"measurements": measurements})


def alerts_list(request):
    alerts = Alert.objects.order_by("-created_on")
    return render(request, "monitoring/alerts_list.html", {"alerts": alerts})