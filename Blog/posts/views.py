from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm

# Create your views here.


def post_create(request):
    form = PostForm(request.POST or None)  # or None : Remember this!
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return HttpResponse("<h1>Saved!</h1>")
    else:
        return render(request, "posts/post_form.html", context={'form': form})


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


def post_update(request, id):
    obj = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=obj)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': obj.title,
        'instance': obj,
        'form': form
    }
    return render(request,"posts/post_form.html",context)

def post_delete(request):
    pass
