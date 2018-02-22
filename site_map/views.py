from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
from blog.models import Post

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    def items(self):
        return ['homepage', 'about', 'reservation']
    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    def items(self):
        return Post.my_query.active()



