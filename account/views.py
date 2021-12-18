from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.conf import settings

from .forms import RegistrationForm, LoginForm, EditForm
from .models import User
from pharmacy.models import Order


def register(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You already authenticated as {user.email}')

    context = {
        'title': 'Register'
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
        'title': 'Login'
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


# def password_reset(request):
#     context = {
#         'title': 'Password Reset'
#     }
#     return render(request, 'account/password_reset.html', context)
#
#
# def password_change(request):
#     context = {
#         'title': 'Change password'
#     }
#     return render(request, 'account/password_change.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')


def profile(request, *args, **kwargs):
    context = {
        'title': 'Profile'
    }
    user = request.user
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


def update_profile(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.id
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse("Something went wrong")
    context = {
        'title': 'Update Profile'
    }
    if request.POST:
        form = EditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = EditForm(request.POST, request.FILES, instance=request.user,
                            initial={
                                "id": user.pk,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "email": user.email,
                                "phone": user.phone,
                                "address": user.address
                            })
            context['edit_form'] = form
    else:
        form = EditForm(request.POST, request.FILES, instance=request.user,
                        initial={
                            "id": user.pk,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "phone": user.phone,
                            "address": user.address
                        })
        # context['edit_form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'account/update_profile.html', context)


def orders(request):
    user_id = request.user.id
    try:
        user = User.objects.get(pk=user_id)
        all_orders = Order.objects.all()
        user_orders = []
        for order in all_orders:
            if order.user == user:
                user_orders.append(order)
    except User.DoesNotExist:
        return HttpResponse("That user doesn't exist")
    context = {
        'title': 'My orders',
        'orders': user_orders,
    }
    return render(request, 'account/orders.html', context)
