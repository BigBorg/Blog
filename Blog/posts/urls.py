from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url("^$", views.post_list),
    url("^create", views.post_create, name="create"),
    url("^detail/(?P<id>\d+)/", views.post_detail, name="detail"),
    url("^list", views.post_list),
    url("^update", views.post_update),
    url("^delete", views.post_delete),
]