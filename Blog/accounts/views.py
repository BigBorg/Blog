from django.shortcuts import render
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from .forms import UserLoginForm, UserRegistrationForm
from Blog.celery_tasks import send_html_email
from .models import Account
from accounts import serializer
import logging
# Create your views here.

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        next = request.GET.get("next")
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect("/")
    return render(request, "accounts/form.html", {"form":form, 'title':"Log in"})

def register_view(request):
    title = "Register"
    form = UserRegistrationForm(request.POST or None)
    context = {
        "title":title,
        "form":form
    }
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        account = Account()
        account.user = user
        account.save()
        new_user = authenticate(username = user.username, password=password)
        login(request,new_user)
        send_html_email.delay(
            from_addr = settings.EMAIL_SMTP_USERNAME,
            to_addr = new_user.email,
            html= settings.EMAIL_ACTIVATION_TEMPLATE.format(username=new_user.username, activation_url=account.get_email_activation_url()),
            subject = "bigborg.top Email Activation"
        )
        next = request.GET.get("next")
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect("/")
    return render(request, "accounts/form.html", context)

def logout_view(request):
    logout(request)
    messages.success(request,"Logged out!")
    return HttpResponseRedirect("/")

def activate_email(request, token):
    try:
        id = serializer.loads(token)
        print(id)
        account = Account.objects.filter(id=id).first()
        user = account.user
    except Exception as e:
        print(e)
        logging.error(str(e))
        raise Http404
    user.account.email_activated = True
    user.account.save()
    messages.success(request, "Email Confirmed!")
    return HttpResponseRedirect("/")