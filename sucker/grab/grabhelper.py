from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from sucker.models import Post, Photo, Topic_site, Tag, Category, Post_category, Post_tag, User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


from django.contrib import messages
from django.shortcuts import redirect

from django.db import IntegrityError
from django.shortcuts import render_to_response

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from os.path import splitext, basename
import requests
import html2text
import sys 
import re
from django_celery_results.models import TaskResult
from datetime import datetime, timedelta
import random
from django.utils import timezone

from django.db.models.aggregates import Count
def clearresu():
	resu = TaskResult.objects.all()
	resu.delete()

def insert_to_db(d):
	# print('inserting')
	result=False
	try:
		newtime=timezone.now()+timedelta(minutes=random.randint(1,60))
		p = Post(
				title=d['title'],
				content=d['content'],
				source=d['url'],
				state=1,
				site= d['site'],
				description=d['description'],
				# tags=d['tags'],
				# category=d['category'],
				publishdate=d['publishdate'],
				id_article=d['id_article'],
				# author= Users.objects.all().exclude(id =1)[random.randint(0,Users.objects.all().exclude(id =1).count()-1)]
				author= User.objects.all().exclude(id =1).order_by('?')[0],
				created_at= newtime,
			)
		p.save()
		bs = BeautifulSoup(d['content'], 'html.parser')
		for img in bs.findAll('img'):
			phd=Photo()
			phd.source= img['src']
			phd.id_post= p.id_post
			phd.save()
			if save_image_from_url(phd,img['src']):
				p.content=p.content.replace(str(phd.source),phd.photo.url)
				p.save()
		for c in d['category'].split('/'):
			if not Category.objects.filter(category=c.lower()).count():
				Category(category=c.lower()).save()
			Post_category(category=Category.objects.get(category=c.lower()), post=p).save()
		for t in d['tags'].split(','):
			if not Tag.objects.filter(tag=t.strip().lower().replace('.', ' ').replace('#', '')).count() and len(t.strip().lower()):
				Tag(tag=t.strip().lower().replace('.', ' ').replace('#', '')).save()
			# asdasd=Tag.objects.get(tag=t.strip().lower().replace('.', ' '))
			# print(asdasd.tag)
			if len(t.strip().lower().replace('.', ' ').replace('#', '')):
				Post_tag(tag=Tag.objects.get(tag=t.strip().lower().replace('.', ' ').replace('#', '')), post=p).save()

		phda=Photo()
		phda.source= d['image']
		phda.id_post= p.id_post
		phda.save()
		if save_image_from_url(phda,d['image']) == True:
			p.image=phda.photo
			p.save()
		result= True
	except Exception as e:
		print(d['tags'])
		result= False
	return result
	
def coba():
	print('ini coba')
	Category(category='asdasd').save()

from os.path import splitext, basename
import requests

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def save_image_from_url(model, url):
    try:
    	r = requests.get(url)
    	img_temp = NamedTemporaryFile()
    	img_temp.write(r.content)
    	img_temp.flush()
    	disassembled = urlparse(url)
    	filename, file_ext = splitext(basename(disassembled.path))
    	model.photo.save('g_'+str(model.id_post)+'_'+str(model.id_photo)+file_ext, File(img_temp), save=True)
    	return True
    except Exception as e:
    	print(e)
    	model.delete()
    	return False
    	
