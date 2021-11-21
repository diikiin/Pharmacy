from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

CATEGORY_CHOICES = (
    'Antibiotics',
    'Antiseptics',
    'Painkillers',
    'Against cough',
    'For baby',
    'Vitamins'
)


class Good(models.Model):
    img = models.ImageField('Image')
    name = models.CharField('Drug name', max_length=50)
    description = models.TextField('Description')
    company = models.CharField('Company manufacturer', max_length=50)
    cost = models.IntegerField('Cost')

    def __str__(self):
        return self.name


class OrderGood(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goods = models.ManyToManyField(OrderGood)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class Contact(models.Model):
    name = models.CharField('Name', max_length=100)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField('Email', max_length=50)
    message = models.TextField('Message')
