from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib import messages
from .models import Post
from .forms import PostForm

# Create your views here.


def post_create(request):
    form = PostForm(request.POST or None)  # or None : Remember this!
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            messages.success(request, '<a href="' + obj.get_absolute_url() + '">' + "Successfully created" + "</a>", extra_tags="html_safe")
            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            messages.error(request, "Not saved.")
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
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    context = {
        "title": "Borg's Blog",
        "object_list": posts#.order_by("-timestamp")
    }
    return render(request, "posts/post_list.html", context)

def post_update(request, id):
    obj = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=obj)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved!")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': obj.title,
        'instance': obj,
        'form': form
    }
    return render(request,"posts/post_form.html",context)

def post_delete(request, id):
    obj = get_object_or_404(Post, id=id)
    obj.delete()
    messages.success(request,"Post deleted")
    return redirect("posts:list")