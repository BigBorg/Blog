from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login', views.login_view, name="login"),
    url(r'^logout', views.logout_view, name="logout"),
    url(r"^register", views.register_view, name="register"),
    url(r"^activate/(?P<token>.*)", views.activate_email, name="activation")
]