from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# HU1 - Login de empresa (NUEVA)
def login_empresa(request):
    """Vista para el login de empresas (HU1)"""
    if request.user.is_authenticated:
        return redirect('monitoring_app:dashboard')
    
    if request.method == 'POST':
        # Usamos el formulario de autenticación pero personalizado para email
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('monitoring_app:dashboard')
        else:
            messages.error(request, 'Correo o contraseña incorrectos')
    
    return render(request, 'usuarios/login_empresa.html')

# HU2 - Registro de empresa (NUEVA)
def registro_empresa(request):
    """Vista para el registro de empresas (HU2)"""
    if request.user.is_authenticated:
        return redirect('monitoring_app:dashboard')
    
    if request.method == 'POST':
        # Datos del formulario
        nombre_empresa = request.POST.get('nombre_empresa')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validaciones básicas
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
        elif User.objects.filter(username=email).exists():
            messages.error(request, 'Ya existe una cuenta con este correo')
        else:
            # Crear el usuario
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password1,
                    first_name=nombre_empresa
                )
                login(request, user)
                messages.success(request, f'¡Empresa {nombre_empresa} registrada exitosamente!')
                return redirect('monitoring_app:dashboard')
            except Exception as e:
                messages.error(request, f'Error en el registro: {str(e)}')
    
    return render(request, 'usuarios/registro_empresa.html')

# Vistas originales (mantener para compatibilidad)
def login_view(request):
    """Vista original de login"""
    if request.user.is_authenticated:
        return redirect('monitoring_app:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('monitoring_app:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})

def registro_view(request):
    """Vista original de registro"""
    if request.user.is_authenticated:
        return redirect('monitoring_app:dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('monitoring_app:dashboard')
        else:
            messages.error(request, 'Error en el registro. Verifica los datos.')
    else:
        form = UserCreationForm()

    return render(request, 'usuarios/registro.html', {'form': form})

def recuperar_contrasena_view(request):
    """Vista para recuperar contraseña"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='usuarios/recuperar_contrasena_email.html',
                subject_template_name='usuarios/recuperar_contrasena_subject.txt'
            )
            messages.success(request, 'Se ha enviado un email con instrucciones para recuperar tu contraseña.')
            return redirect('usuarios:login_empresa')  # Cambiado a login_empresa
    else:
        form = PasswordResetForm()

    return render(request, 'usuarios/recuperar_contrasena.html', {'form': form})

@login_required
def dashboard_view(request):
    """Dashboard de usuario - Redirige al dashboard de monitoring"""
    return redirect('monitoring_app:dashboard')

def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('usuarios:login_empresa')  # Cambiado a login_empresa