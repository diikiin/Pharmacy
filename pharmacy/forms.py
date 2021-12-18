from .models import Item, Contact
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class GoodForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['img', 'name', 'description', 'company', 'cost']


class ContactForm(forms.ModelForm):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.Textarea()

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


PAYMENT_CHOICES = (
    ('C', 'Cash'),
    ('On', 'Online')
)


class CheckoutForm(forms.Form):
    address = forms.CharField(required=False)
    name = forms.TextInput()
    phone = PhoneNumberField()
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
