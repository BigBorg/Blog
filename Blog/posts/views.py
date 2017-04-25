from urllib.parse import quote_plus
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment
# Create your views here.


def post_create(request):
    if not request.user.is_staff and not request.user.is_superuser:
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
    if obj.draft or not obj.published <= timezone.now().date():
        if not request.user.is_staff and not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(obj.content.encode("utf-8"))

    initial_data = {
        'object_id' : obj.id,
        'content_type':obj.get_content_type
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        if isinstance(request.user, AnonymousUser):
            return HttpResponseForbidden("<h1>You need to log in</h1>")
        ctype = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=ctype)
        obj_id = form.cleaned_data.get("object_id")
        content = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()

        comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content,
            parent = parent_obj
        )

        if created:
            messages.success(request,"Comment Created!")
        return HttpResponseRedirect(comment.content_object.get_absolute_url())

    context = {
        'title': obj.title,
        'obj': obj,
        'share_string': share_string,
        'comment_form': form
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

    page = request.GET.get('page') or 1
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
    if not request.user.is_staff and not request.user.is_superuser:
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
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    obj = get_object_or_404(Post, slug=slug)
    obj.delete()
    messages.success(request,"Post deleted")
    return redirect("posts:list")
