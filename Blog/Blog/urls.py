from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from posts.views import post_list
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # Examples:
    # url(r'^$', 'Blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^posts/', include("posts.urls", namespace="posts")),
    url(r'^comments/', include("comments.urls", namespace="comments")),
    url(r'^accounts/', include("accounts.urls", namespace="accounts")),
    url(r'^api/posts/', include("posts.api.urls", namespace="posts-api")),
    url(r'^api/comments/', include("comments.api.urls", namespace="comments-api")),
    url(r"^api/accounts/", include("accounts.api.urls", namespace="accounts-api")),
    url(r'^api/token-auth/', obtain_jwt_token),
    url(r"^$", post_list)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)