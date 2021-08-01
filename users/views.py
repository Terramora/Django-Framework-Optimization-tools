from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from django.contrib import auth, messages
from django.urls import reverse
from baskets.models import Basket
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


def registrations(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_link(user):
                messages.success(request, 'Регистрация успешна!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'title': 'Регистрация',
               'form': form}
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'Личный кабинет',
               'form': form,
               'baskets': Basket.objects.filter(user=request.user)}
    return render(request, 'users/profile.html', context)


def verify(request, email, activation_key):
    user = User.objects.filter(email=email).first()
    if user:
        if user.active_key == activation_key and not user.active_key_expired():
            user.is_active = True
            user.save()

            messages.success(request, 'Аккаунт успешно подтвержден!')
        else:
            messages.success(request, 'Аккаунт не подтвержден')

        return HttpResponseRedirect(reverse('users:login'))

    return HttpResponseRedirect(reverse('index'))


def send_verify_link(user):
    subj = 'Verify ur account'
    link = reverse('users:verify', args=[user.email, user.active_key])
    message = f'{settings.DOMAIN}{link}'
    return send_mail(subject=subj, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])
