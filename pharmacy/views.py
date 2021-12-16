from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from account.models import User
from .forms import ContactForm, CheckoutForm
from .models import Item, OrderItem, Order

navigation = [{'title': 'Home', 'url_name': 'home'},
              {'title': 'About us', 'url_name': 'about'},
              {'title': 'Contact', 'url_name': 'contact'},
              {'title': 'Catalog', 'url_name': 'catalog'},
              {'title': 'Cart', 'url_name': 'cart'},
              {'title': 'Account'}]


def index(request):
    context = {
        'navigation': navigation,
        'title': 'Home',
        'items': Item.objects.all()[:6],
        'special': Item.objects.get(special__exact=True)
    }
    return render(request, 'pharmacy/index.html', context)


def about(request):
    context = {
        'navigation': navigation,
        'title': 'About us'
    }
    return render(request, 'pharmacy/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = request.POST.get('name')
            message = request.POST.get('message')
            email = request.POST.get('email')
            send_mail(subject, message, email, [settings.EMAIL_HOST_USER])

    context = {
        'navigation': navigation,
        'title': 'Contact'
    }
    return render(request, 'pharmacy/contact.html', context)


class CatalogView(ListView):
    model = Item
    template_name = 'pharmacy/catalog.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navigation'] = navigation
        context['title'] = 'Catalog'
        return context


class SearchView(ListView):
    model = Item
    template_name = 'pharmacy/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navigation'] = navigation
        context['title'] = 'Catalog'
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Item.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )
        return object_list


class ItemDetailView(DetailView):
    model = Item
    template_name = 'pharmacy/good.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navigation'] = navigation
        return context


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'objects': order,
                'navigation': navigation,
                'title': 'Cart'
            }
            return render(self.request, 'pharmacy/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cart")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart")


def delete_order(request, pk):
    order = Item.objects.get(pk=pk)
    order.delete()
    return redirect('orders')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'navigation': navigation,
                'form': form,
                'order': order,
            }
            return render(self.request, "pharmacy/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("cart")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                order.address = self.request.POST.get('address')
                order.phone = self.request.POST.get('phone')
                order.name = self.request.POST.get('name')
                order.payment_option = self.request.POST.get('payment_option')
                order.ordered = True
                order.save()
                return redirect('home')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("cart")
