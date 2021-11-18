from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Good(models.Model):
    img = models.ImageField('Image')
    name = models.CharField('Drug name', max_length=50)
    description = models.TextField('Description')
    company = models.CharField('Company manufacturer', max_length=50)
    cost = models.IntegerField('Cost')


class Contact(models.Model):
    name = models.CharField('Name', max_length=100)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField('Email', max_length=50)
    message = models.TextField('Message')
