from django.contrib import admin
from .models import Post, PostCategory, PostTags
from mptt.admin import DraggableMPTTAdmin
from django.db.models import F
# Register your models here.


def active_deactive(modeladmin, request, queryset):
    for ele in queryset:
        if ele.active:
            ele.active = False
            ele.save()
        else:
            ele.active = True
            ele.save()
active_deactive.short_description = 'Ενεργοποίηση/ Απενεργοποίηση'


def check_announcement(modeladmin, request, queryset):
    for ele in queryset:
        if not ele.announcement:
            ele.announcement = True
            ele.save()
        else:
            ele.announcement = False
            ele.save()
check_announcement.short_description = 'Ενεργοποίηση/Απενεργοποίησης Ανακοίνωσης'


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'show_homepage', 'announcement', 'category','publish', 'updated']
    list_filter = ['active','announcement', 'category', 'publish', 'updated', 'show_homepage']
    search_fields = ['updated', 'publish', 'title', 'title_eng']
    readonly_fields = ['publish','image_tag']
    actions = [active_deactive, check_announcement]
    fieldsets = (
        (None, {
            'fields': (('active','show_homepage'), ('announcement', 'active_english'),('image_tag','image'), ('category', 'tags'), ('publish', 'updated'))
        }),
        ('Ελληνικά', {
            'fields': (('title', 'content'))
        }),
        ('Αγγλικά', {
            'fields': ('title_eng', 'content_eng')
        }),
        ('SEO', {
            'fields': ('slug',
                       ('seo', 'meta_description'),
                       ('keywords_eng', 'meta_description_eng'))
        }),
    )


class PostsTagsAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_eng']

admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, DraggableMPTTAdmin)
admin.site.register(PostTags, PostsTagsAdmin)