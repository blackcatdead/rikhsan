# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from django_celery_results.models import TaskResult
from sucker.models import Photo, Post, Post_category, Post_tag, Category, Tag
# Create your views here.

from sucker.grab import grabhelper, kompas, liputan6, quote
def develop(request):
	data={}
	# data= liputan6.artikel("https://www.liputan6.com/bola/read/3577173/jadwal-babak-8-besar-piala-dunia-2018")
	# data= liputan6.visit()
	# data= kompas.artikel("https://entertainment.kompas.com/read/2018/06/21/090337010/penggemar-bts-dan-beyonce-gelar-pesta-streaming-bareng")
	# data= kompas.visit()
	
	# grabhelper.coba()
	# return JsonResponse(data, safe=False)
	# data= kompas.artikel("https://tekno.kompas.com/read/2018/07/06/18430047/ini-merek-yang-dipakai-go-jek-di-vietnam-dan-thailand")
	# data = kompas.visitTopic('https://tekno.kompas.com/',5)
	# data= quote.grabquote()
	#done
	data= liputan6.visitTopic('https://www.liputan6.com/fashion-beauty',100)
	return HttpResponse(str(data))

def develop2(request):
	data =1;
	template = loader.get_template('develop.html')
	context = {
        'data': data,
    }
	return HttpResponse(template.render(context, request))
	
def resetdatabase(request):
	# TaskResult.objects.all().delete()
	Post_category.objects.all().delete()
	Post_tag.objects.all().delete()
	Category.objects.all().delete()
	Tag.objects.all().delete()
	Photo.objects.all().delete()
	Post.objects.all().delete()