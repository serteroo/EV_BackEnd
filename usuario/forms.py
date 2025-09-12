from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Correo', required=True)
    company_name = forms.CharField(label='Nombre de la empresa', max_length=150)

    class Meta:
        model = User
        fields = ('email', 'company_name', 'password1', 'password2')
