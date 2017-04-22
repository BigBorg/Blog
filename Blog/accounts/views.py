from django.shortcuts import render
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .forms import UserLoginForm, UserRegistrationForm

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
        new_user = authenticate(username = user.username, password=password)
        login(request,new_user)
        next = request.GET.get("next")
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(request,"/")
    return render(request, "accounts/form.html", context)

def logout_view(request):
    logout(request)
    messages.success(request,"Logged out!")
    return HttpResponseRedirect("/")