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


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use')

    def save(self, commit=True):
        user = super(EditForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return self.cleaned_data
                else:
                    self.add_error("password", forms.ValidationError("Password is wrong"))
            except User.DoesNotExist:
                self.add_error("email", forms.ValidationError("User does not exist"))
