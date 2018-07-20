# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from sucker.models import Post, Photo, Post_category,Category, Post_tag, Tag, User
from django.core.paginator import Paginator
from django.db.models import Count
from datetime import datetime, timedelta
from django.utils import timezone
def terbaru(request, page=1):
	data =1;
	template = loader.get_template('v_terbaru.html')
	context = {
        'data': data,
        'posts': getlatest(10,page),
        'tags': toptags(15),
        'penulis': getpenulis(6,1,True),
        'populer': toppost(10,1),
        'page': page,
        
    }
	return HttpResponse(template.render(context, request))
	
def post(request,idd,judul):
	artikel= Post.objects.get(id_post=idd)
	# print(str(artikel.created_at)+' - '+str(timezone.now())+' = '+str((timezone.now()-artikel.created_at).days))
	artikel.viewed = artikel.viewed + 1
	artikel.save()
	template = loader.get_template('v_singlepost.html')
	context = {
		'page': 'Artikel',
		'populer': toppost(10,1),
        'post': artikel,
        'terbaru': getlatest(5,1),
        'tags': toptags(15),
        'randomposts':randompost(6,artikel.id_post),
        'penulis': getpenulis(4,1,True),
    }
	return HttpResponse(template.render(context, request))

def showcategory(request,cate,page=1):
	template = loader.get_template('v_category.html')
	context = {
		'page': 'Category',
        'posts': getcategory(cate,10,page),
        'category': cate,
        'terbaru': getlatest(5,1),
        'tags': toptags(15),
        'page': page,
        'populer': toppost(10,1),
		'penulis': getpenulis(4,1,True),
    }
	return HttpResponse(template.render(context, request))
	
def showtag(request,tag,page=1):
	template = loader.get_template('v_tag.html')
	context = {
		'page': 'Category',
        'posts': gettag(tag,10,page),
        'tag': tag.replace('-',' '),
        'terbaru': getlatest(5,1),
        'tags': toptags(15),
        'page': page,
        'populer': toppost(10,1),
		'penulis': getpenulis(4,1,True),
    }
	return HttpResponse(template.render(context, request))

def showsite(request,site,page=1):
	template = loader.get_template('v_site.html')
	context = {
		'page': 'Site',
        'posts': getsite(site.replace('-',' '),10,page),
        'site': site.replace('-',' '),
        'terbaru': getlatest(5,1),
        'tags': toptags(15),
        'page': page,
    }
	return HttpResponse(template.render(context, request))

def showauthor(request,page=1):
	template = loader.get_template('v_allauthor.html')
	context = {
		'page': 'All Author',
        # 'posts': getsite(site.replace('-',' '),10,page),
        'populer': toppost(10,1),
        'author': getpenulis(12,page),
        'terbaru': getlatest(5,1),
        'tags': toptags(15),
        'page': page,

    }
	return HttpResponse(template.render(context, request))

def author(request, id_author, page=1):
	template = loader.get_template('v_author.html')
	autho = User.objects.get(id=id_author)
	context = {
		'page': 'Author',
        # 'posts': getsite(site.replace('-',' '),10,page),
        'author': autho,
        'populer': toppost(10,1),
        'terbaru': getlatest(5,1),
        'tags': toptags(15),
        'authorpost': getauthorpost(5,page,autho),
    }
	return HttpResponse(template.render(context, request))

def kontak(request):
	template = loader.get_template('v_contact.html')
	context = {
		'page': 'Kontak',
    }
	return HttpResponse(template.render(context, request))

def disclaimer(request):
	template = loader.get_template('v_disclaimer.html')
	context = {
		'page': 'Disclaimer',
    }
	return HttpResponse(template.render(context, request))

def aturandanprivasi(request):
	template = loader.get_template('v_aturan_dan_privasi.html')
	context = {
		'page': 'Aturan dan Privasi',
    }
	return HttpResponse(template.render(context, request))

def alltag(request):
	template = loader.get_template('v_alltag.html')
	context = {
		'page': 'Semua Tag',
		'alltag': Tag.objects.filter(post_tag__post__created_at__lte=timezone.now()).annotate(coun=Count('post_tag')).values('tag','coun').order_by('tag'),
		# 'tags': toptags(15),
		'terbaru': getlatest(5,1),
        'penulis': getpenulis(6,1,True),
        'populer': toppost(10,1),
    }
	return HttpResponse(template.render(context, request))

def allcategory(request):
	
	template = loader.get_template('v_allcategory.html')
	context = {
		'page': 'Semua Kategori',
		'allcatagory': Category.objects.filter(post_category__post__created_at__lte=timezone.now()).annotate(coun=Count('post_category')).values('category','coun').order_by('category'),
    	'tags': toptags(15),
        'penulis': getpenulis(6,1,True),
        'populer': toppost(10,1),
    }

	return HttpResponse(template.render(context, request))

def pencarian(request, page=1):
	result=[]
	query= ''
	template = loader.get_template('v_pencarian.html')

	if request.GET.get('page'):
		page = request.GET['page']

	if request.GET.get('q'):
		query = request.GET['q']
		result = getpencarian(10,page,query)

	
	print(result.count)
	context = {
		'page': page,
		'posts': result,
    	'tags': toptags(15),
        'penulis': getpenulis(6,1,True),
        'populer': toppost(10,1),
        'query': query,
    }
	return HttpResponse(template.render(context, request))



from django.shortcuts import render
 
 
def error_404(request):
	template = loader.get_template('404.html')
	context = {
		'page': '404',
	}
	return HttpResponse(template.render(context, request))
 
def error_500(request):
    template = loader.get_template('500.html')
    context = {
    	'page': '500',
    }
    return HttpResponse(template.render(context, request))

# ==============================================================================================================
def getcategory(cat=None,limit=None,page=None):
	post_category =[];
	# post_category= Post_category.objects.filter(category=Category.objects.get(category=cat)).order_by('-id_post_category')
	post_category= Post_category.objects.select_related('post').filter(post__created_at__lte=timezone.now()).filter(category=Category.objects.get(category=cat)).order_by('-post__created_at')

	p = Paginator(post_category, limit)
	# for x in artikels:
	# 	print(x.post.title)
	return p.page(page)

def getlatest(limit,page):
	berita_terbaru =[];
	berita_terbaru= Post.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')
	p = Paginator(berita_terbaru, limit)
	return  p.page(page)

def toppost(limit,page):
	terpopuler =[];
	terpopuler= Post.objects.filter(created_at__lte=timezone.now()).order_by('-viewed')
	p = Paginator(terpopuler, limit)
	return  p.page(page)

def gettag(ta,limit,page):
	post_tag =[];
	post_tag= Post_tag.objects.select_related('post').filter(post__created_at__lte=timezone.now()).filter(tag=Tag.objects.get(tag=ta.replace('-',' '))).order_by('-post__created_at')

	p = Paginator(post_tag, limit)
	# for x in artikels:
	# 	print(x.post.title)
	return p.page(page)

def getsite(sit,limit,page):
	berita_site =[];
	berita_site= Post.objects.filter(site=sit).filter(created_at__lte=timezone.now()).order_by('-created_at')
	p = Paginator(berita_site, limit)
	return p.page(page)

def toptags(limit=None):
	q= Post_tag.objects.select_related('post').filter(post__created_at__lte=timezone.now()).values('tag').annotate(coun=Count('tag')).values('tag_id__tag','coun').order_by('-coun')[:limit]
	if limit != None:
		q=q[:limit]
	return q

def randompost(limit=1, id_po=0):
	rando =[];
	rando= Post.objects.exclude(id_post=id_po).filter(created_at__lte=timezone.now()).order_by('?')[:limit]
	return rando

def getpenulis(limit,page,rand=False):
	penulis=[]
	penulis= User.objects.all().exclude(id =1).order_by('?' if rand else 'username')
	p = Paginator(penulis, limit)
	return p.page(page)

def getauthorpost(limit,page,autho):
	authorpost=[]
	authorpost=Post.objects.filter(created_at__lte=timezone.now()).filter(author= autho).order_by('-created_at')
	p = Paginator(authorpost, limit)
	return p.page(page)

def getpencarian(limit, page, q):
	pencarian=[]
	pencarian=Post.objects.filter(created_at__lte=timezone.now()).filter(title__icontains=q).order_by('-created_at')
	p = Paginator(pencarian, limit)
	return p.page(page)