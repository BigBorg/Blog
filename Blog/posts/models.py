from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from markdown2 import markdown
from unidecode import unidecode
from .utils import count_words


def upload_location(instance, filename):
    PostModel = instance.__class__
    try:
        new_id = PostModel.objects.order_by("id").last().id + 1
    except:
        new_id = 1
    return "%s/%s" % (new_id, filename)


class ActivePostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(ActivePostManager, self).filter(draft=False, published__lte=timezone.now().date())


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, null=True, max_length=120)
    image = models.ImageField(null=True, blank=True,
                              upload_to=upload_location,
                              width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    published = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now triggered when model.save() called
    timestamp = models.DateTimeField(auto_now=False,
                                     auto_now_add=True)  # auto_now_add triggered when object first created
    num_chinese = models.IntegerField(default=0)
    num_english = models.IntegerField(default=0)
    objects = ActivePostManager()

    def __str__(self):  # __unicode__ for py2
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def get_api_url(self):
        return reverse("posts-api:detail", kwargs={"slug": self.slug})

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

    @property
    def comments(self):
        from comments.models import Comment
        instance = self
        return Comment.objects.filter_by_instance(instance)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    class Meta:
        ordering = ['-published', '-updated']


def create_slug(instance, new_slug=None):
    slug = slugify(unidecode(instance.title))
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def pre_save_subscriber(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    chinese, english = count_words(instance.get_markdown())
    instance.num_chinese = chinese
    instance.num_english = english


def post_delete_subscriber(sender, instance, *args, **kwargs):
    if instance.image:
        instance.image.delete(False)


pre_save.connect(pre_save_subscriber, Post)
post_delete.connect(post_delete_subscriber, Post)
