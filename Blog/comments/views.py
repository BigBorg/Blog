from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse_lazy
from models import Comment
from forms import CommentForm
# Create your views here.

@login_required()
def comment_delete(request, id):
    obj = get_object_or_404(Comment,id=id)
    if request.method=='POST':
        if obj.user != request.user:
            return HttpResponseForbidden("<h1>This comment was not created by you!</h1>")
        post_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Comment deleted!")
        return HttpResponseRedirect(post_url)

    context = {
        "object":obj
    }
    return render(request, "comments/delete.html",context)

def comment_thread(request, id):
    comment = get_object_or_404(Comment, id=id)
    if not comment.is_parent:
        comment = comment.parent
    initial_data = {
        'content_type':comment.content_type,
        'object_id':comment.object_id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
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

    return render(request,"comments/thread.html", {
        'comment':comment,
        'comment_form':form
    })