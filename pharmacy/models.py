from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('Antibiotics', 'Antibiotics'),
    ('Antiseptics', 'Antiseptics'),
    ('Painkillers', 'Painkillers'),
    ('Against cough', 'Against cough'),
    ('For baby', 'For baby'),
    ('Vitamins', 'Vitamins')
)


class Item(models.Model):
    img = models.ImageField('Image')
    name = models.CharField('Drug name', max_length=50)
    description = models.TextField('Description')
    company = models.CharField('Company manufacturer', max_length=50)
    cost = models.IntegerField('Cost')
    discount = models.BooleanField('Discount')
    discount_cost = models.IntegerField('Discount cost', default=0)
    special = models.BooleanField('Special', default=False)
    special_cost = models.IntegerField('Special cost', default=0)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)
    quantity = models.IntegerField(default=1)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_special_percent(self):
        return int(100 - (self.special_cost / self.cost) * 100)

    def get_absolute_url(self):
        return reverse("item", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_cost(self):
        return self.quantity * self.item.cost

    def get_total_discount_item_cost(self):
        return self.quantity * self.item.discount_cost

    def get_total_special_item_cost(self):
        return self.quantity * self.item.special_cost

    def get_amount_saved(self):
        if self.item.discount:
            return self.get_total_item_cost() - self.get_total_discount_item_cost()
        else:
            return self.get_total_item_cost() - self.get_total_special_item_cost()

    def get_final_cost(self):
        if self.item.discount:
            return self.get_total_discount_item_cost()
        elif self.item.special:
            return self.get_total_special_item_cost()
        return self.get_total_item_cost()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    address = models.CharField(blank=True, null=True, max_length=100)
    phone = PhoneNumberField(null=True, blank=True)
    payment = models.CharField(blank=True, null=True, max_length=20)

    def __str__(self):
        return self.user.email

    def get_total_cost(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_cost()
        return total

    def delete_order_url(self):
        return reverse("delete-order", kwargs={
            'pk': self.pk
        })


class Contact(models.Model):
    name = models.CharField('Name', max_length=100)
    email = models.EmailField('Email', max_length=50)
    message = models.TextField('Message')
