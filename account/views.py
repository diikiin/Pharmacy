from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout

from .forms import RegistrationForm, LoginForm
from .models import User

navigation = [{'title': 'Home', 'url_name': 'home'},
              {'title': 'About us', 'url_name': 'about'},
              {'title': 'Contact', 'url_name': 'contact'},
              {'title': 'Catalog', 'url_name': 'catalog'},
              {'title': 'Cart', 'url_name': 'cart'},
              {'title': 'Account'}]


def register(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You already authenticated as {user.email}')

    context = {
        'navigation': navigation
    }

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            auth_login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('profile')
        else:
            context['registration_form'] = form

    return render(request, 'account/registration.html', context)


def login(request, *args, **kwargs):
    context = {
        'navigation': navigation
    }

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
            else:
                context['login_form'] = form

    return render(request, 'account/login.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get("next"))
    return redirect


def password_reset(request):
    context = {
        'navigation': navigation
    }
    return render(request, 'account/reset_password.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')


def profile(request, *args, **kwargs):
    context = {
        'navigation': navigation
        }
    user=request.user
    user_id = user.id
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse("That user doesn't exist")
    if user:
        context['id'] = user.id
        context['email'] = user.email
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['phone'] = user.phone
        context['address'] = user.address
    return render(request, 'account/profile.html', context)


def password_change(request):
    context = {
        'navigation': navigation
    }
    return render(request, 'account/reset_password.html', context)


def orders(request):
    context = {
        'navigation': navigation
    }
    return render(request, 'account/orders.html', context)
