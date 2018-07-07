"""multisite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from iota import views
from django.contrib.sitemaps.views import sitemap
from iota.sitemaps import BlogSitemap, TagSitemap, CategorySitemap
from django.conf.urls import handler404, handler500

sitemaps ={
    'posts': BlogSitemap,
}

sitemaps2 ={
    'categories' : CategorySitemap,
}

sitemaps3 ={
    'tags' : TagSitemap,
}


urlpatterns = [
   
    url(r'^terbaru/([0-9]+)', views.terbaru, name='terbaru'),
    url(r'^terbaru/', views.terbaru, name='terbaru'),
    url(r'^$', views.terbaru, name='home'),
    url(r'^artikel/([0-9]+)/()', views.post, name='artikel'),
    
    url(r'^category/([\w\-]+)/([0-9]+)', views.showcategory, name='category'),
    url(r'^category/([\w\-]+)', views.showcategory, name='category'),
    url(r'^tag/([\w\-]+)/([0-9]+)', views.showtag, name='tag'),
    url(r'^tag/([\w\-]+)', views.showtag, name='tag'),
    url(r'^site/([\w\-]+)/([0-9]+)', views.showsite, name='site'),
    url(r'^site/([\w\-]+)', views.showsite, name='site'),
    url(r'^allauthor/([\w\-]+)', views.showauthor, name='allauthor'),
    url(r'^allauthor/', views.showauthor, name='allauthor'),
     url(r'^author/([\w\-]+)/([\w\-]+)', views.author, name='author'),
    url(r'^author/([\w\-]+)', views.author, name='author'),
   

    url(r'^alltag', views.alltag, name='alltag'),
    url(r'^allcategory', views.allcategory, name='allcategory'),

    url(r'^kontak/', views.kontak, name='kontak'),
    url(r'^disclaimer/', views.disclaimer, name='disclaimer'),
    url(r'^kebijakanprivasi/', views.aturandanprivasi, name='kebijakanprivasi'),

    url(r'^sitemap/post.xml$', sitemap, {'sitemaps': sitemaps}, name='post_sitemap'),
    url(r'^sitemap/category.xml$', sitemap, {'sitemaps': sitemaps2}, name='category_sitemap'),
    url(r'^sitemap/tag.xml$', sitemap, {'sitemaps': sitemaps3}, name='tag_sitemap'),

    url(r'^pencarian', views.pencarian, name='pencarian'),

    # url(r'^test404', views.error_404, name='404'),
]

# handler404 = views.error_404
# handler500 = views.error_500

from django.conf import settings
from django.views.static import serve
# if settings.DEBUG:
urlpatterns +=[
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]

# urlpatterns +=[
#     url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}),
# ]