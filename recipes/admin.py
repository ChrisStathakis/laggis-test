from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin
# Register your models here.


def active_or_deactive(modeladmin, request, queryset):
    for ele in queryset:
        if ele.active == False:
            ele.active = True
            ele.save()
        else:
            ele.active = False
            ele.save()
active_or_deactive.short_description = 'Ενεργοποίηση/Απενεργοποίηση'


class CategoryRecipeAdmin(DraggableMPTTAdmin):
    actions = [active_or_deactive]
    list_filter = ['active']
    #list_display = ['title', 'title_eng', 'active']
    fieldsets = (
        (None, {
            'fields': ('active',)
        }),
        ('Ελληνικά', {
            'fields': ('title','text'),
        }),
        ('Αγγλικά', {
            'fields': ('title_eng', 'text_eng'),
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('slug', ('seo_title', 'seo_description', 'seo_keywords'), ('seo_title_eng', 'seo_description_eng', 'seo_keywords_eng')),
        }),
    )


class RecipeAdmin(admin.ModelAdmin):
    actions = [active_or_deactive]
    search_fields = ['title', 'title_eng', 'text', 'text_eng']
    list_filter = ['active', 'category']
    list_display = ['image_tag_tiny', 'title', 'title_eng', 'price', 'category', 'active']
    readonly_fields = ['image_tag', 'black_image_tag', 'image_tag_tiny']
    fieldsets = (
        (None, {
            'fields': ('active', ('image_tag', 'image', 'black_image_tag', 'black_image'), ('price', 'category', 'by_order'))
        }),
        ('Ελληνικά', {
            'fields': ('title', 'text'),
        }),
        ('Αγγλικά', {
            'fields': ('title_eng', 'text_eng'),
        }),
        ('Πρωτη Σελίδα', {
            'fields': (('is_special_item'),),
        }),
        ('SEO', {
            'classes':('collapse',),
            'fields': ('slug', ('seo_title', 'seo_description', 'seo_keywords'), ('seo_title_eng', 'seo_description_eng', 'seo_keywords_eng')),
        }),
    )


admin.site.register(RecipeCategory, CategoryRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)