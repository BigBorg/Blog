from urllib import quote_plus
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from .models import Post
from .forms import PostForm
# Create your views here.


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)  # or None : Remember this!
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, '<a href="' + obj.get_absolute_url() + '">' + "Successfully created" + "</a>", extra_tags="html_safe")
            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            messages.error(request, "Not saved.")
            return render(request, "posts/post_form.html", context={'form': form})
    else:
        return render(request, "posts/post_form.html", context={'form': form})


def post_detail(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if obj.draft or not obj.published < timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(obj.content)
    content_type = ContentType.objects.get_for_model(Post)
    object_id = obj.id
    comments = Comment.objects.filter(content_type=content_type, object_id=object_id)
    context = {
        'title': obj.title,
        'obj': obj,
        'share_string': share_string,
        'comments': comments
    }
    return render(request, "posts/detail.html", context)


def post_list(request):
    if request.user.is_staff or request.user.is_superuser:
        posts_list = Post.objects.all()
    else:
        posts_list = Post.objects.active()

    query = request.GET.get("q")
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)|
            Q(content__icontains=query)
        )
    paginator = Paginator(posts_list, 10) # Show 25 contacts per page

    page = request.GET.get('page') or 0
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
        "object_list": posts,
        "today": timezone.now().date()
    }
    return render(request, "posts/post_list.html", context)

def post_update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
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

def post_delete(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    obj = get_object_or_404(Post, slug=slug)
    obj.delete()
    messages.success(request,"Post deleted")
    return redirect("posts:list")