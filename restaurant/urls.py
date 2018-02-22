from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from homepage.views import *
from django.contrib.sitemaps.views import sitemap
from site_map.views import *

sitemaps = {
    'static_hm': StaticViewSitemap,
    'blog': PostSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view=Homepage.as_view(), name='homepage'),
    url(r'^about/$', RedirectView.as_view(url='/', permanent=False), name='about'),
    url(r'^reservation/$', ReservationPage.as_view(), name='reservation'),
    url(r'^menu/$', MenuPage.as_view(), name='menu'),
    url(r'^menu/(?P<slug>[-\w]+)/$', MenuPageDetails.as_view(), name='menu_detail'),
    url(r'^blog/$', BlogPageGre.as_view(), name='blog'),
    url(r'^contact/$', ContactPage.as_view(), name='contact'),
    url(r'^blog/(?P<slug>[-\w]+)/$', BlogDetail.as_view(), name='blog_detail'),
    url(r'^set-english/$', view=switch_to_English_link, name='eng_cookie'),
    url(r'^set-greek/$', view=switch_to_Greek_link, name='gre_cookie'),

    url(r'^en/$', HomepageEng.as_view(), name='homepage_eng'),
    url(r'^en/about/$', RedirectView.as_view(url='/', permanent=False), name='about_eng'),
    url(r'^en/reservation/$', ReservationPageEng.as_view(), name='reservation_eng'),
    url(r'^en/menu/$', MenuPageEng.as_view(), name='menu_eng'),
    url(r'^en/menu/(?P<slug>[-\w]+)/$', MenuPageDetailsEng.as_view(), name='menu_detail_eng'),
    url(r'^en/blog/$', BlogPageEng.as_view(), name='blog_eng'),
    url(r'^en/contact/$', ContactPageEng.as_view(), name='contact_eng'),
    url(r'^en/blog/(?P<slug>[-\w]+)/$', BlogDetailEng.as_view(), name='blog_detail_eng'),
    url(r'^set-english/$', view=switch_to_English_link, name='eng_cookie'),
    url(r'^set-greek/$', view=switch_to_Greek_link, name='gre_cookie'),
    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', include('robots.urls')),

    #url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index'),
    url(r'^cache-clear/', view=cache_clear, name='cache_clear'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)