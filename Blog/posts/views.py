from django.http import HttpResponse
from django.shortcuts import render
from .models import Post

# Create your views here.


def post_create(request):
    pass


def post_detail(request):
    pass


def post_list(request):
    context = {
        "title": "Borg's Blog",
        "object_list": Post.objects.all()
    }
    return render(request, "posts/index.html", context)


def post_update(request):
    pass


def post_delete(request):
    pass
