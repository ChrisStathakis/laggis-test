from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField
# Create your models here.

MAX_POST_SIZE_FILE = 0.5*1024*1024


def validate_image(value):
    if value.file.size > MAX_POST_SIZE_FILE:
        return ValidationError('Το αρχείο είναι μεγαλύτερο από 0,5mb.')
    return value


def upload_file(instance, filename):
    return 'blog/%s/%s'%(instance.title, filename)


def upload_file_gallery(instance, filename):
    return 'gallery/%s/%s'%(instance.title, filename)


class PostTags(models.Model):
    title = models.CharField(max_length=100,)
    title_eng = models.CharField(max_length=100,default='English')

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title


class PostCategory(MPTTModel):
    title = models.CharField(max_length=100, unique=True, )
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    content = models.CharField(max_length=150, null=True, blank=True)
    title_eng = models.CharField(max_length=100, default='English')
    parent = TreeForeignKey('self', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Κατηγορία blog'

    def __str__(self):
        return self.title

    def posts_count(self):
        return Post.objects.filter(category=self).count()


class PostManager(models.Manager):
    def active(self):
        return super(PostManager, self).filter(active=True)

    def return_last_five(self):
        return super(PostManager, self).all()[0:5]

    def active_announcements(self):
        return super(PostManager, self).filter(active=True, announcement=True)

    def active_and_english_post(self):
        return super(PostManager, self).filter(active = True, active_english=True)

    def active_and_english_announcement(self):
        return super(PostManager, self).filter(active = True, active_english=True, announcement=True)

    def show_homepage(self):
        return super(PostManager, self).filter(active=True, show_homepage=True)

    def show_homepage_eng(self):
        return super(PostManager, self).filter(active=True, show_homepage=True, active_english=True)


class Post(models.Model):
    show_homepage = models.BooleanField(default=True, verbose_name='Εμφάνιση στην αρχική σελίδα')
    active = models.BooleanField(default=True)
    active_english = models.BooleanField(default=False, verbose_name='Εμφάνιση στην Αγγλική Version')
    title = models.CharField(max_length=100, verbose_name='Τίτλος')
    image = models.ImageField(upload_to=upload_file, validators=[validate_image, ], help_text='Το μέγεθος πρέπει να είναι μέχρι 0,5 mb')
    content = HTMLField(verbose_name='Κείμενο', null=True)
    publish = models.DateField(auto_now=True, auto_now_add=False, verbose_name='Ημερομηνία Δημιουργίας')
    updated = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Ημερομηνία Event/Παρουσίασης')
    slug = models.SlugField(unique=True,null=True, blank=True, allow_unicode=True, verbose_name='Slug - Dont bother with that ')
    category = models.ForeignKey(PostCategory, null=True, verbose_name='Κατηγορία')
    tags = models.ManyToManyField(PostTags, null=True, blank=True)
    announcement = models.BooleanField(default=False, verbose_name='Ανακοίνωση')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    title_eng = models.CharField(max_length=100, verbose_name='Title', default='English tile')
    content_eng = HTMLField(verbose_name='Short description or Intro', default='English text', null=True,)
    # seo
    seo = models.CharField(max_length=100, blank=True, verbose_name='Keywords')
    meta_description = models.CharField(max_length=100, blank=True, verbose_name='Description')
    keywords_eng = models.CharField(max_length=100, blank=True, verbose_name='English Keywords')
    meta_description_eng = models.CharField(max_length=100, blank=True, verbose_name='English Description')

    my_query = PostManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Blog'
        ordering = ['-updated']

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.image))

    def image_tag_tiny(self):
        return mark_safe('<img width="50px" height="50px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.image))
    image_tag_tiny.short_description = 'Image'

    def absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug':self.slug})


class Gallery(models.Model):
    image = models.ImageField(upload_to=upload_file_gallery, validators=[validate_image,])
    post_related = models.ForeignKey(Post)

    def __str__(self):
        return '%s %s' % (self.post_related.title, self.id)

    def image_tag_tiny(self):
        return mark_safe(
            '<img width="50px" height="50px" src="https://laggis.s3.amazonaws.com/media/%s" />' % (self.image))
    image_tag_tiny.short_description = 'Image'