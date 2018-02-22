from django.db import models
import datetime
# Create your models here.


class ContactInfo(models.Model):
    # the real contact model
    date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Ημερομηνία Δημιουργίας')
    name = models.CharField(max_length=255, verbose_name='Ονοματεπώνυμο')
    phone = models.CharField(max_length=10, blank=True, null=True, verbose_name='Τηλέφωνο')
    email = models.EmailField(blank=True, null=True,)
    message = models.TextField(verbose_name='Μήνυμα', blank=True, null=True)
    is_readed = models.BooleanField(default=False, verbose_name='Το έχεις δει;')

    class Meta:
        verbose_name_plural = '2. Επικοινωνία'

    def __str__(self):
        return self.name


class ContactInfoPage(models.Model):
    open_time = models.CharField(default='Ωρες Λειτουργίας', max_length=160, verbose_name='Τίτλος, Ωρες Λειτουργίας στα Ελληνικά')
    address = models.CharField(default='Διεύθυνση', max_length=160, verbose_name='Τίτλος Διεύθυνση στα Ελληνικά')
    address_text = models.TextField(default='', verbose_name='Κείμενο Διεύθυνση στα Ελληνικά')
    support = models.CharField(default='Support', verbose_name='Τίτλος Ωρες support στα Ελληνικά', max_length=160)
    support_text = models.TextField(default='', verbose_name='Κείμενο support στα Ελληνικά')
    open_time_eng = models.CharField(default='Ωρες Λειτουργίας', max_length=160, verbose_name='Τίτλος, Ωρες Λειτουργίας στα Αγγλικά')
    address_eng = models.CharField(default='Διεύθυνση', max_length=160, verbose_name='Τίτλος Διεύθυνση στα Αγγλικά')
    address_text_eng = models.TextField(default='', verbose_name='Κείμενο Διεύθυνση στα Αγγλικά')
    support_eng = models.CharField(default='Support', verbose_name='Τίτλος Ωρες support στα Αγγλικά', max_length=160)
    support_text_eng = models.TextField(default='', verbose_name='Κείμενο support στα Αγγλικά')

    class Meta:
        verbose_name_plural = '4. Διαχείριση Πληροφορίες Contact Page'

    def __str__(self):
        return self.open_time


class Contact(models.Model):
    #that used for reservations
    date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Ημερομηνία Δημιουργίας')
    name = models.CharField(max_length=255, verbose_name='Ονοματεπώνυμο')
    phone = models.CharField(blank=True, null=True, verbose_name='Τηλέφωνο', max_length=10)
    email = models.EmailField(blank=True, null=True,)
    people = models.IntegerField(default=2, verbose_name="'Ατομα")
    message = models.TextField(verbose_name='Μήνυμα', blank=True, null=True)
    resever_date = models.CharField(max_length=50, default='05/02/17', verbose_name='Ημερομηνία Κράτησης')
    time = models.CharField(verbose_name="'Ωρα Κράτησης", max_length=15)
    is_readed = models.BooleanField(default=False, verbose_name='Το έχεις δει;')

    class Meta:
        verbose_name_plural = '1. Κρατήσεις'

    def __str__(self):
        return self.name


class ReservationInfo(models.Model):
    active = models.BooleanField(default=True)
    left_title = models.CharField(default='Αριστερός τίτλος στα Ελληνικά', max_length=160, verbose_name='Τίτλος στα Ελληνικά')
    right_title = models.CharField(default='Δεξιός τίτλος στα Ελληνικά', max_length=160, verbose_name='Τίτλος στα Αγγλικά')
    seo_keywords = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')
    seo_keywords_eng = models.CharField(max_length=160, default='Εστιατόριο, Λακωνία')
    seo_description_eng = models.CharField(max_length=160, default='Μία παραδοσιακή ψαροταβέρνα...')

    class Meta:
        verbose_name_plural = '3. Διαχείριση σελίδας Reservation'

    def __str__(self):
        return self.left_title