from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .models import Post, PostCategory, PostTags
from unidecode import unidecode


def create_slug(instance,new_slug=None):
    text = unidecode((instance.title).lower())
    slug = slugify(text)
    if new_slug is not None:
        slug=new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s'%(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug


@receiver(post_save, sender=Post)
def create_unique_slug(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        instance.save()
    if not instance.seo:
        instance.seo = 'Εστιατόριο, Λακωνία, Ψαροταβέρνα, %s' % instance.title
        instance.save()
    if not instance.meta_description:
        instance.meta_description = 'Η Ψαροταβέρνα Διαμαντής σας καλωσοριζεί στο Post με τον τίτλο %s' % instance.title
    if not instance.keywords_eng:
        instance.keywords_eng = 'Εστιατόριο, Λακωνία, Ψαροταβέρνα, %s' % instance.title
        instance.save()
    if not instance.meta_description_eng:
        instance.meta_description_eng = 'Η Ψαροταβέρνα Διαμαντής σας καλωσοριζεί στο Post με τον τίτλο %s' % instance.title
        instance.save()
post_save.connect(create_unique_slug, sender=Post)


@receiver(post_save, sender=PostCategory)
def create_slug_post_cat(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        instance.save()

post_save.connect(create_slug_post_cat, sender=PostCategory)

