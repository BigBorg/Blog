from django.conf.urls import url
from . import views

urlpatterns = [
    url("^$", views.post_list, name="list"),
    url("^list", views.post_list),
    url("^create", views.post_create, name="create"),
    url("^(?P<slug>[\w-]+)/$", views.post_detail, name="detail"),
    url("^(?P<slug>[\w-]+)/edit", views.post_update, name="update"),
    url("^(?P<slug>[\w-]+)/delete", views.post_delete, name="delete"),
]