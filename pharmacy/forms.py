from .models import Good, Contact
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['img', 'name', 'description', 'company', 'cost']


class ContactForm(forms.ModelForm):
    name = forms.CharField()
    phone = PhoneNumberField()
    email = forms.EmailField()
    message = forms.Textarea()

    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message']