from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import Good, OrderGood, Order

navigation = [{'title': 'Home', 'url_name': 'home'},
              {'title': 'About us', 'url_name': 'about'},
              {'title': 'Contact', 'url_name': 'contact'},
              {'title': 'Catalog', 'url_name': 'catalog'},
              {'title': 'Cart', 'url_name': 'cart'},
              {'title': 'Account'}]


class IndexView(ListView):
    model = Good
    template_name = 'pharmacy/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navigation'] = navigation
        context['title'] = 'Home'
        return context


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


def catalog(request):
    context = {
        'navigation': navigation,
        'title': 'Catalog',
        'goods': Good.objects.all()
    }
    return render(request, 'pharmacy/catalog.html', context)


class GoodDetailView(DetailView):
    model = Good
    template_name = 'pharmacy/good.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navigation'] = navigation
        return context


def cart(request):
    context = {
        'navigation': navigation,
        'title': 'Cart'
    }
    return render(request, 'pharmacy/cart.html', context)


def add_to_cart(request, slug):
    item =get_object_or_404(Good, slug=slug)
    order_good=OrderGood.objects.create(item=item)