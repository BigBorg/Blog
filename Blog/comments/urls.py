from django.conf.urls import url
from . import views

urlpatterns = [
    url("^(?P<id>\d+)/$", views.comment_thread, name="thread"),
    #url("^(?P<slug>[\w-]+)/de   lete", views.post_delete, name="delete"),
]