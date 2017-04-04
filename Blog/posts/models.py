from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now triggered when model.save() called
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)  # auto_now_add triggered when object first created

    def __str__(self):  # __unicode__ for py2
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    class Meta:
        ordering= ['-timestamp', '-updated']