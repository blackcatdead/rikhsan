from django.contrib.sitemaps import Sitemap
from sucker.models import Post,Tag,Category
from datetime import datetime
from django.db.models import Count

class BlogSitemap(Sitemap):
    def items(self):
        return Post.objects.filter(created_at__lte=datetime.now()).order_by('-id_post')[:100]


class TagSitemap(Sitemap):
    def items(self):
        return Tag.objects.all().order_by('tag')

class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all().order_by('category')



