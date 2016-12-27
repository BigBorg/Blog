from django.contrib import admin
from .models import Post
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Post

    list_display = ['title', 'updated', 'timestamp']
    list_display_links = ['updated']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'content']
    list_editable = ['title']

admin.site.register(Post, PostModelAdmin)
