from django.db import models
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField
# Create your models here.

MAX_SIZE_FILE = 1024*1024


def validate_image(value):
    if value.file.size > MAX_SIZE_FILE:
        return ValidationError('το αρχείο είναι μεγαλύτερο από 1 mb')


def upload_file(instance, filename):
    return 'recipes/%s/%s'%(instance.title, filename)


class RecipeCategoryManager(models.Manager):
    def active_categories(self):
        return super(RecipeCategoryManager, self).filter(active= True)

    def first_page_and_active(self):
        return super(RecipeCategoryManager, self).filter(active=True, is_special_item=True)


class RecipeCategory(MPTTModel):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, verbose_name='Όνομασια')
    title_eng = models.CharField(max_length=100, verbose_name='Όνομασια στα Eng')
    #  icon = models.ImageField(upload_to=upload_file, blank=True, null=True,)
    #  image = models.ImageField(blank=True, null=True,verbose_name='Εικόνα', upload_to=upload_file, blank=True)
    #  black_image = models.ImageField(blank=True, null=True, verbose_name='Σκίτσο', upload_to=upload_file)
    text = HTMLField(null=True, blank=True, verbose_name='Περιγραφή')
    text_eng = HTMLField(blank=True, null=True, verbose_name='Περιγραφή στα Eng')
    #  is_first_page = models.BooleanField(default=True, verbose_name='Εμφάνιση στην Αρχική Σελίδα')
    slug = models.CharField(null=True, blank=True, max_length=160)
    seo_title = models.CharField(null=True, blank=True, max_length=60)
    seo_description = models.CharField(null=True, blank=True, max_length=160)
    seo_keywords = models.CharField(null=True, blank=True, max_length=160)
    seo_title_eng = models.CharField(null=True, blank=True, max_length=60)
    seo_description_eng = models.CharField(null=True, blank=True, max_length=160)
    seo_keywords_eng = models.CharField(null=True, blank=True, max_length=160)
    by_order = models.IntegerField(default=1)
    parent = TreeForeignKey('self', blank=True, null='True', )
    objects = models.Manager()
    my_query = RecipeCategoryManager()

    class Meta:
        ordering =['by_order']
        verbose_name_plural ='Κατηγορίες Συνταγών'

    def __str__(self):
        return self.title
    '''
    def image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.image))

    def black_image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.black_image))

    def image_tag_tiny(self):
        return mark_safe('<img width="50px" height="50px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.image))
    image_tag_tiny.short_description = 'Image'
    '''


class RecipeManager(models.Manager):
    def active_items(self):
        return super(RecipeManager, self).filter(active=True)

    def special_item(self):
        return super(RecipeManager, self).filter(active=True, is_special_item=True)

    def specific_category(self, id):
        return super(RecipeManager, self).filter(category__id=id)


class Recipe(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, verbose_name='Ονομασία')
    title_eng = models.CharField(max_length=100, verbose_name='Ονομασία στα Eng')
    image = models.ImageField(blank=True, null=True,
                              verbose_name='Εικόνα ',
                              upload_to=upload_file,
                              validators=[validate_image, ],
                              help_text='Το αρχείο πρέπει να είναι μικρότερο από 1 mb'
                              )
    black_image = models.ImageField(blank=True,
                                    null=True,
                                    verbose_name='Σκίτσο',
                                    upload_to=upload_file,
                                    validators=[validate_image, ],
                                    help_text='Το αρχείο πρέπει να είναι μικρότερο από 1 mb',
                                    )
    text = HTMLField(blank=True, null=True, verbose_name='Περιγραφή')
    text_eng = HTMLField(blank=True, null=True, verbose_name='Περιγραφή στα Eng')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6, verbose_name='Τιμή')
    category = models.ForeignKey(RecipeCategory, verbose_name='Κατηγορία')
    slug = models.CharField(null=True, blank=True, max_length=160,)
    #  show_first_page = models.BooleanField(default=True, verbose_name='Εμφάνιση στο Μενού στην Αρχική Σελίδα')
    is_special_item = models.BooleanField(default=False, verbose_name='Εμφάνιση στα Special στην Αρχική Σελίδα')
    seo_title = models.CharField(null=True, blank=True, max_length=60)
    seo_description = models.CharField(null=True, blank=True, max_length=160)
    seo_keywords = models.CharField(null=True, blank=True, max_length=160)
    seo_title_eng = models.CharField(null=True, blank=True, max_length=60)
    seo_description_eng = models.CharField(null=True, blank=True, max_length=160)
    seo_keywords_eng = models.CharField(null=True, blank=True, max_length=160)
    by_order = models.IntegerField(default=1, verbose_name='Ταξινόμηση')
    objects = models.Manager()
    my_query = RecipeManager()

    class Meta:
        ordering =['by_order']
        verbose_name_plural='Συνταγές'

    def __str__(self):
        return self.title

    def check_image(self):
        if self.image:
            return self.image.url
        return 'static/assets/images/seafood/kingcrab.png'

    def check_black_image(self):
        if self.black_image:
            return self.image.url
        return '/../../static/assets/images/seafood/clamp.png'

    def image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.image))

    def black_image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.black_image))

    def image_tag_tiny(self):
        return mark_safe('<img width="50px" height="50px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.image))
    image_tag_tiny.short_description = 'Image'



