from django.conf.urls import url
from comments import views

urlpatterns = [
    url("^(?P<id>\d+)/$", views.comment_thread, name="thread"),
    url("^(?P<id>\d+)/delete", views.comment_delete, name="delete"),
]