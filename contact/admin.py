from django.contrib import admin
from .models import Contact, ReservationInfo,ContactInfoPage, ContactInfo
import csv
from django.http import HttpResponse
# Register your models here.




def export_reservations(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reservations.csv"'
    writer = csv.writer(response)
    writer.writerow(['Ημερομηνία', 'Ώρα', 'Ονοματεπώνυμο', 'Άτομα', 'Τήλεφωνο' , 'Email', 'Μήνυμα'])
    reservations = queryset.values_list('resever_date', 'time', 'name', 'people', 'phone' , 'email', 'message')
    for resever in reservations:
        writer.writerow(resever)
    return response

export_reservations.short_description = 'Εξαγωγή επιλέγμένων'

def contact_is_readed(modeladmin, request, queryset):
    for ele in queryset:
        if ele.is_readed == False:
            ele.is_readed = True
            ele.save()
        else:
            ele.is_readed = True
            ele.save()

contact_is_readed.short_description = 'Διαβασμένο'

class ReservationInfoAdmin(admin.ModelAdmin):
    list_display = ('left_title', 'active')
    list_filter = ('active',)
    fieldsets = (
        ('Βασικά Στοιχεία', {
            'fields':('active', ('left_title', 'right_title'),('seo_keywords', 'seo_keywords_eng'),('seo_description','seo_description_eng'))
        }),
    )

class ContactInfoPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Στα Ελληνικά', {
            'fields':('open_time',('address','address_text'),('support', 'support_text'))
        }),
        ('Στα Αγγλικά', {
            'fields':('open_time_eng',('address_eng','address_text_eng'),('support_eng', 'support_text_eng'))
        }),
    )

class ContactAdmin(admin.ModelAdmin):
    actions = [contact_is_readed, export_reservations]
    search_fields = ['resever_date', 'name', 'email', 'phone']
    list_display = ['resever_date', 'time', 'name', 'people', 'email', 'date','is_readed']
    fields = ['is_readed', 'resever_date', 'time', 'name', 'email', 'message', 'phone', 'date']
    list_filter = ['is_readed', 'date']
    readonly_fields = ['date','message', 'phone' ]

class ContactInfoAdmin(admin.ModelAdmin):
    actions = [contact_is_readed]
    search_fields = ['name', 'email', 'date', 'phone']
    list_display = ['name','email','date','is_readed']
    fields = ['is_readed', 'name', 'email', 'message', 'phone', 'date']
    list_filter = ['is_readed', 'date']
    readonly_fields = ['date','message', 'phone' ]


admin.site.register(Contact, ContactAdmin)
admin.site.register(ReservationInfo, ReservationInfoAdmin)
admin.site.register(ContactInfoPage, ContactInfoPageAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)