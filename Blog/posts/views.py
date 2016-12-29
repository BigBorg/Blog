from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.


def post_create(request):
    pass


def post_detail(request, id):
    obj = get_object_or_404(Post, id=id)
    context = {
        'title': obj.title,
        'obj': obj
    }
    return render(request, "posts/detail.html", context)


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
