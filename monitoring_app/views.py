from django.shortcuts import render, get_object_or_404
from .models import Organization, Category, Zone, Device, Measurement, Alert
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def dashboard(request):
    organizations = Organization.objects.all()
    categories    = Category.objects.all()
    zones         = Zone.objects.all()
    devices       = Device.objects.all()
    measurements  = Measurement.objects.all()[:10]   # Últimas 10 mediciones
    alerts        = Alert.objects.filter(status="ACTIVE")  # Solo alertas activas

    
    critical_alerts = (
        alerts.filter(
            Q(severity__iexact="CRITICAL") |
            Q(severity__iexact="GRAVE") |      
            Q(severity__iexact="CRÍTICO")
        )
        .order_by("-created_at")[:5]           
    )

    context = {
        "organizations": organizations,
        "categories": categories,
        "zones": zones,
        "devices": devices,
        "measurements": measurements,
        "alerts": alerts,
        "critical_alerts": critical_alerts,
    }
    return render(request, "monitoring/dashboard.html", context)


def devices_list(request):
    category_id = request.GET.get("category")
    zone_id = request.GET.get("zone")

    q = (request.GET.get("q") or "").strip()

    devices = Device.objects.all()
    if category_id and category_id != "all":
        devices = devices.filter(category_id=category_id)
    if zone_id and zone_id != "all":
        devices = devices.filter(zone_id=zone_id)

    context = {
        "devices": devices,
        "categories": Category.objects.all(),
        "zones": Zone.objects.all(),

        "selected_category": category_id,
        "selected_zone": zone_id,
        "q": q,
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


@login_required
def measurements_list(request):
    # Trae todas las mediciones (más recientes primero)
    qs = Measurement.objects.order_by("-measured_at")

    # Paginación: 20 por página
    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # maneja páginas inválidas también

    context = {
        "page_obj": page_obj,
        "measurements": page_obj.object_list,   # por compatibilidad con tu template
        "is_paginated": page_obj.has_other_pages(),
    }
    return render(request, "monitoring/measurements_list.html", context)



def alerts_list(request):
    alerts = Alert.objects.order_by("-created_on")
    return render(request, "monitoring/alerts_list.html", {"alerts": alerts})


@login_required
def organization_profile(request):
    org = None

    if hasattr(request.user, "organization") and request.user.organization:
        org = request.user.organization

    elif hasattr(request.user, "profile") and getattr(request.user.profile, "organization", None):
        org = request.user.profile.organization
    else:
        org = Organization.objects.first()
    devices_count = 0
    if org:
        try:
           
            devices_count = Device.objects.filter(category__organization=org).count()
        except Exception:
            
            devices_count = Device.objects.filter(organization=org).count()

    context = {
        "org": org,
        "devices_count": devices_count,
    }
    return render(request, "monitoring/organization_profile.html", context)