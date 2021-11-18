from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login

from .models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=60)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

        def clean_email(self):
            email = self.cleaned_data['email'].lower()
            try:
                account = User.objects.get(email=email)
            except Exception as e:
                return email
            raise forms.ValidationError(f'Email {email} is already in use')


class LoginForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")

