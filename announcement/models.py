from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.

def upload_file(instance, filename):
    return 'announcement/%s/%s'%(instance.title, filename)

class AnnouncementTag(models.Model):
    title = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.title

class AnnouncementManager(models.Manager):
    def active_next_30_days(self,):
        date_now = datetime.now()
        next_30_days = date_now + timedelta(days=30)
        return super(AnnouncementManager, self).filter(date_expire__range=['%s'%(date_now),'%s'%(next_30_days)], active=True)

class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name='Τίτλος')
    publish= models.DateTimeField(auto_now_add=True, verbose_name='Ημερομηνία Δημιουργίας')
    image = models.ImageField(null=True, upload_to=upload_file, help_text='Width:300px, height:200px')
    date_start = models.DateTimeField(default=datetime.now(), verbose_name='Ημερομηνία Έναρξης')
    date_expire = models.DateTimeField(default=datetime.now(), verbose_name='Ημερομηνία Λήξης')
    text = models.TextField(verbose_name='Περιγραφή')
    tags = models.ManyToManyField(AnnouncementTag)
    active = models.BooleanField(default=True, verbose_name='Ορατό Στην Κεντρική σελίδα')

    my_query = AnnouncementManager()
    objects = models.Manager()

    class Meta:
        ordering = ['date_expire']
    def __str__(self):
        return self.title
