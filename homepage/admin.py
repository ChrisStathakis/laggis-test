from django.contrib import admin
from .models import *
# Register your models here.


class AboutSkillsInline(admin.TabularInline):
    model = AboutSkills
    extra = 3


class AboutBannerInline(admin.TabularInline):
    model = AboutBanner
    extra = 3


class StaffInline(admin.TabularInline):
    model = Staff
    extra = 3


class OpenHoursInline(admin.TabularInline):
    model = OpenHours
    extra = 2


class TableOpensTimesInline(admin.TabularInline):
    model = TableOpenTimes
    extra = 5


class AboutSkillsAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_eng', 'active', ]
    list_filter = ['active']


class StaffAdmin(admin.ModelAdmin):
    list_display = ['image_tag_tiny','title', 'title_eng','occupation', 'active']
    list_filter = ['active', 'occupation']
    readonly_fields = ['image_tag']
    fields = ['active', 'image_tag', 'icon', 'occupation', 'text', 'title_eng', 'occupation_eng', 'text_eng', 'page_related']


class IndexPageAdmin(admin.ModelAdmin):
    readonly_fields = ['menu_image_tag', 'about_image_tag', 'table_image_tag']
    inlines = [OpenHoursInline, TableOpensTimesInline]
    fieldsets = (
        ('Menu', {
            'fields':('active', ('title', 'title_eng',),
                      ('menu_image_tag', 'menu_image'),
                      ('describe', 'describe_eng'),
                      ('color_menu_li', 'color_menu_hover')
                      )
        }),
        ('About',{
            'fields':(('about_image_tag', 'about_image'),
                      ('about_us', 'about_us_eng'))
        }),
        ('Reservation',{
            'fields':(('table_image_tag', 'table_image'),
                      )
        }),
        ('SEO',{
            'fields':(('seo_keywords', 'seo_description'),
                      ('seo_keywords_eng', 'seo_description_eng'))
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        #  Disable delete
        actions = super(IndexPageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class MenuPageInfoAdmin(admin.ModelAdmin):
    readonly_fields = ['image_tag', 'catalogue_image_tag']
    fields = ('active',
              ('title', 'title_eng'),
              ('image_tag', 'image'),
              ('catalogue_image_tag', 'catalogue'),
              ('seo_keywords', 'seo_description', 'seo_keywords_eng', 'seo_description_eng'),
              )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        #  Disable delete
        actions = super(MenuPageInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class BlogPageInfoAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        #  Disable delete
        actions = super(BlogPageInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ['active']
    inlines = [AboutSkillsInline, AboutBannerInline, StaffInline ]
    fieldsets = (
        ('Βασικά', {
            'fields': ('active', ('title', 'title_eng'),
                       ('text', 'text_eng'),
                       ('seo_keywords', 'seo_description'),
                       ('seo_keywords_eng', 'seo_description_eng'),
                       )
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        # Disable delete
        actions = super(AboutPageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        # Disable delete
        actions = super(BannerAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(OpenHours)
admin.site.register(IndexPage, IndexPageAdmin)
#admin.site.register(Banner)
#admin.site.register(AboutPage, AboutPageAdmin)
#admin.site.register(Staff, StaffAdmin)
#admin.site.register(AboutSkills, AboutSkillsAdmin)
admin.site.register(TableOpenTimes)
#admin.site.register(AboutBanner)
admin.site.register(MenuPageinfo, MenuPageInfoAdmin)
admin.site.register(BlogPageinfo, BlogPageInfoAdmin)
