from django.shortcuts import render
from .forms import ContactForm

navigation = [{'title': 'Home', 'url_name': 'home'},
              {'title': 'About us', 'url_name': 'about'},
              {'title': 'Contact', 'url_name': 'contact'},
              {'title': 'Catalog', 'url_name': 'catalog'},
              {'title': 'Cart', 'url_name': 'cart'},
              {'title': 'Account'}]


def index(request):
    context = {
        'navigation': navigation,
        'title': 'Home'
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
            form.save()

    context = {
        'navigation': navigation,
        'title': 'Contact'
    }
    return render(request, 'pharmacy/contact.html', context)


def catalog(request):
    context = {
        'navigation': navigation,
        'title': 'Catalog'
    }
    return render(request, 'pharmacy/catalog.html', context)


def cart(request):
    context = {
        'navigation': navigation,
        'title': 'Cart'
    }
    return render(request, 'pharmacy/cart.html', context)
