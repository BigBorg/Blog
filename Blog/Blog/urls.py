from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from posts.views import post_list

urlpatterns = [
    # Examples:
    # url(r'^$', 'Blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^posts/', include("posts.urls", namespace="posts")),
    url(r'^comments/', include("comments.urls", namespace="comments")),
    url(r'^accounts/', include("accounts.urls", namespace="accounts")),
    url(r"^$", post_list)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)