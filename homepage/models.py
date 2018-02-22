from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
# Create your models here.


def validate_image_size(value):
    if value.file.size > 1024*1024*0.5:
        raise ValidationError('This file is bigger than 0.5 mb')


def upload_photo(instance,filename):
    return 'about/{0}/{1}'.format(instance.title, filename)


class IndexPage(models.Model):
    title = models.CharField(default='Εστιατόριο Ψαροταβέρνα Ο Διαμαντής', max_length=100, verbose_name='Τίτλος')
    menu_image = models.ImageField(upload_to=upload_photo, blank=True, null=True, verbose_name='Είκονα Banner', help_text='1250px*1112px', validators=[validate_image_size,])
    describe = models.CharField(default='Μια οικογενιακή επειχήρηση ταν ταν', max_length=200)
    describe_eng = models.CharField(default='The Seafood Restaurant has been voted by locals as "Best in the area" year after year. We actively seek out the freshest in regional seafood and produce our restaurant.Μν' ,max_length=200)
    active = models.BooleanField(default=True)
    about_image = models.ImageField(upload_to=upload_photo, null=True, verbose_name='Είκονα About', validators=[validate_image_size,])
    table_image = models.ImageField(upload_to=upload_photo, null=True, verbose_name='Είκονα Κλείσε Τραπέζι', validators=[validate_image_size,])
    about_us = models.TextField(help_text='<p class="text">', default='Greek Version')
    about_us_eng = models.TextField(help_text='<p class="text">', default='English Version')
    seo_keywords = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')
    title_eng = models.CharField(default='Restaurant Diamantis', max_length=100, verbose_name='Title English')
    seo_keywords_eng = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description_eng = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')
    color_menu_li = models.CharField(max_length=20, default='#e3e3e3', help_text='Εάν το αφήσεις κενο παίρνει το αρχικό', null=True, blank=True, verbose_name='Χρώμα menu επιλεγμένο')
    color_menu_hover = models.CharField(max_length=20, default='#e3e3e3', help_text='Εάν το αφήσεις κενο παίρνει το αρχικό', null=True, blank=True, verbose_name='Χρώμα menu ')

    class Meta:
        verbose_name_plural = '1. Διαχείριση Αρχικής Σελίδας'

    def __str__(self):
        return self.title

    def menu_image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.menu_image))

    def about_image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.about_image))

    def table_image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.table_image))


class Banner(models.Model):
    active = models.BooleanField(default=True,)
    title = models.CharField(default='default', max_length=60)
    text = models.TextField(default='default')
    title_eng = models.CharField(default='default', max_length=60)
    text_eng = models.TextField(default='default')
    page_related = models.ForeignKey(IndexPage, null=True)

    class Meta:
        verbose_name_plural ='2. Διαχείριση Κινούμενου Banner'

    def __str__(self):
        return self.title


class Events(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateTimeField()
    text = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class OpenHours(models.Model):
    title = models.CharField(max_length=150, default='Δευτέρα - Παρασκευή', verbose_name='Ωρες')
    title_eng = models.CharField(max_length=150, default='Monday - Friday', verbose_name='Ωρες-Eng')
    open = models.CharField(max_length=10, verbose_name='Ανοίγουμε.')
    close = models.CharField(max_length=10, verbose_name='κλείνουμε.')
    order_by = models.IntegerField(default=1, verbose_name='Κατάταξη')
    active = models.BooleanField(default=True)
    page_related = models.ForeignKey(IndexPage, null=True)

    class Meta:
        verbose_name_plural = '3. Διαχείριση Ωρών Λειτουργίας'
        ordering = ['order_by']

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=upload_photo, null=True)
    title = models.CharField(default='Η ΙΣΤΟΡΙΑ ΜΑΣ', max_length=150, verbose_name='Ονομασία στα Ελληνικά')
    text = models.TextField(default='Greek', verbose_name='Περιγραφή στα Ελληνικά', help_text='<p class="text">')
    title_eng = models.CharField(default='OUR STORY', max_length=150, verbose_name='Ονομασία στα Αγγλικά')
    text_eng = models.TextField(default='English', verbose_name='Περιγραφή στα Αγγλικά')
    seo_keywords = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')
    seo_keywords_eng = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description_eng = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')

    class Meta:
        verbose_name_plural = '4. About - Σχετικά Με Εμάς'

    def __str__(self):
        return self.title


class AboutSkills(models.Model):
    active = models.BooleanField(default=True)
    icon = models.CharField(max_length=150, help_text='http://fontawesome.io/icons/')
    title = models.CharField(max_length=60, default='Greek', verbose_name='Ονομασία στα Ελληνικά')
    text = models.TextField(default='Greek', verbose_name='Περιγραφή στα Ελληνικά')
    title_eng = models.CharField(max_length=60, default='English', verbose_name='Ονομασία στα Αγγλικά')
    text_eng = models.TextField(default='English', verbose_name='Περιγραφή στα Αγγλικά')
    page_related = models.ForeignKey(AboutPage, null=True)

    class Meta:
        verbose_name_plural = '5. About - Services on About Page'

    def __str__(self):
        return self.title


class AboutBanner(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=160)
    title_eng = models.CharField(max_length=50)
    text_eng = models.CharField(max_length=160)
    icon = models.CharField(max_length=50)
    page_related = models.ForeignKey(AboutPage)

    class Meta:
        verbose_name_plural='7. About- Banner Text'

    def __str__(self):
        return self.title


class Staff(models.Model):
    active = models.BooleanField(default=True)
    icon = models.ImageField(upload_to=upload_photo, null=True, verbose_name='Φωτογραφία', help_text='260*350' )
    title = models.CharField(max_length=60, default='Greek', verbose_name='Ονομασία στα Ελληνικά')
    occupation = models.CharField(max_length=100, default='Greek', verbose_name='Απασχόληση στα Ελληνικά')
    text = models.TextField(default='Greek', verbose_name='Περιγραφή στα Ελληνικά')
    title_eng = models.CharField(max_length=60, default='English', verbose_name='Ονομασία στα Αγγλικά')
    occupation_eng = models.CharField(max_length=100, default='Greek', verbose_name='Απασχόληση στα Αγγλικά')
    text_eng = models.TextField(default='English', verbose_name='Περιγραφή στα Αγγλικά')
    page_related = models.ForeignKey(AboutPage, null=True)

    class Meta:
        verbose_name_plural = '6. About - Προσωπικό'

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.icon))

    def image_tag_tiny(self):
        return mark_safe('<img width="50px" height="50px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.icon))
    image_tag_tiny.short_description = 'Φωτογραφία'


class TableOpenTimes(models.Model):
    title = models.CharField(max_length=30, default='Δευτέρα')
    title_eng = models.CharField(max_length=30,)
    times = models.CharField(max_length=30,)
    page_related = models.ForeignKey(IndexPage, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '4. Διαχείριση Πίνακα Ωρών'


class MenuPageinfo(models.Model):
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=upload_photo, null=True, blank=True, verbose_name='Banner photo', validators=[validate_image_size,])
    catalogue = models.ImageField(upload_to=upload_photo, blank=True, null=True, verbose_name='Φωτογραφία καταλόγου', validators=[validate_image_size,])
    title = models.CharField(default='Blog', max_length=150, verbose_name='Ονομασία στα Ελληνικά')
    title_eng = models.CharField(default='Blog', max_length=150, verbose_name='Ονομασία στα Αγγλικά')
    seo_keywords = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')
    seo_keywords_eng = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description_eng = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')

    class Meta:
        verbose_name_plural = '5. Seo Σελίδας Menu'

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.image))

    def catalogue_image_tag(self):
        return mark_safe('<img width="150px" height="150px" src="https://laggis.s3.amazonaws.com/media/%s" />' %(self.catalogue))


class BlogPageinfo(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(default='Menu', max_length=150, verbose_name='Ονομασία στα Ελληνικά')
    title_eng = models.CharField(default='Menu', max_length=150, verbose_name='Ονομασία στα Αγγλικά')
    seo_keywords = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')
    seo_keywords_eng = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description_eng = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')

    class Meta:
        verbose_name_plural = '6. Seo Σελίδας Blog'

    def __str__(self):
        return self.title



