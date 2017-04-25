from django import forms
import datetime
from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    published = forms.DateField(widget=forms.SelectDateWidget(years=range(1985, datetime.date.today().year+10)))
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            'draft',
            'published',
            "content"
        ]