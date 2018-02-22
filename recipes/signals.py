from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from unidecode import unidecode
from .models import Recipe


@receiver(post_save, sender=Recipe)
def create_slug_title(sender, instance, *args, **kwargs):
    if not instance.slug:
        title = slugify(unidecode(instance.title))
        exists = Recipe.objects.filter(slug=title)
        if exists:
            title = title + '%s' % instance.id
        instance.slug = title
        instance.save()
post_save.connect(create_slug_title, sender=Recipe)

