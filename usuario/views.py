from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignUpForm
from monitoring_app.models import Organization  # ya existe en tu app

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            company = form.cleaned_data['company_name']

            # Usamos el email como username
            user = User.objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data['password1']
            )

            Organization.objects.create(name=company)

            login(request, user)
            messages.success(request, 'Registro exitoso.')
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'usuario/register.html', {'form': form})
