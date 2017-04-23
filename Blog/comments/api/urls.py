from django.conf.urls import url
from views import CommentListAPIView, CommentDetailAPIView, CommentCreateAPIView, CommentEditAPIView

urlpatterns = [
    url(r"^$", CommentListAPIView.as_view(), name="list"),
    url(r"^(?P<id>\d+)/$", CommentDetailAPIView.as_view(), name="thread"),
    url(r"create", CommentCreateAPIView.as_view(), name="create"),
    url(r"^(?P<id>\d+)/edit$", CommentEditAPIView.as_view(), name="edit"),
]