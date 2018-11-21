# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, get_user_model, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import account_activation_token
from auctions.models import Auction, User
from .forms import LoginForm, RegisterForm, EditProfileForm, PasswordChangeForm
from .models import Profile


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    # print("User logged in")
    # print(request.user.is_authenticated())
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:

            print("Error")
    return render(request, 'accounts/login.html', context)


user = get_user_model()


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Auc-tion Account'
            message = render_to_string(
                'accounts/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(subject, message)
            return redirect('account_activation_sent')

    else:
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


def activate_page(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        profil = Profile()
        profil.user = user
        # profil.email =
        user.save()
        profil.user = user
        profil.email = request.POST['email']
        profil.bio  = request.POST['bio']
        profil.birth_date = request.POST['birth_date']
        profil.address = request.POST['address']
        profil.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


def my_profile_page(request):
    my_auctions = Auction.objects.filter(creata_da__username=request.user.username)
    m_user = Profile.objects.get(user=request.user)
    my_offer = Auction.objects.filter(id__in=m_user.mine_partecipated.all()).order_by('-scadenza')

    messages = m_user.show_messages

    context = {
        'my_auction': my_auctions,
        'my_offer': my_offer,
        'messages': messages}
    return render(request, 'accounts/profile_page.html', context=context)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')





@login_required
def profile_page(request):
    my_auction = Auction.objects.filter(vendor__username=request.user.username)
    m_user = Profile.objects.get(user = request.user)
    my_offer = Auction.objects.filter(id__in= m_user.mine_auctions.all()).order_by('-deadline')
    mess = m_user.show_messages

    context = {
        'my_auction': my_auction,
        'my_offer': my_offer,
        'messages': mess
    }
    return render(request, 'accounts/profile_page.html', context)


def edit_profile_page(request):
    inst = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile')
        else:
            return redirect('/accounts/edit_profile_page')
    else:

        form = EditProfileForm(instance=request.user.profile)
        context = {
            'form': form
        }
        return render(request, 'accounts/edit_profile.html', context)


def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/accounts/profile')
        else:
            return redirect('/account/change_password')
    else:
        form = PasswordChangeForm(instance=request.user)
        context = {
              'form': form
        }
        return render(request, 'accounts/change_password.html', context)


def show_my_notifications(request):
    m_mess = Profile.objects.get(user=request.user).show_messages
    if request.method == 'POST':
        m_mess.all().delete()
        return HttpResponseRedirect('/accounts/profile_page/')
    else:
        context = {
            'messages': m_mess.order_by('time')
        }
        return render(request, 'accounts/notification.html', context)



