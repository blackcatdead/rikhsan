# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
# from sorl.thumbnail import ImageField
from slugify import slugify
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils import timezone
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib import admin
from django.db.models.aggregates import Count
from random import randint

from django.db import models
from django.contrib.auth.models import AbstractUser
from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import reverse

class User(AbstractUser):
    avatar= models.ImageField(blank=True, null=True, upload_to='users')
    description = models.TextField(blank=True, null=True)
    image_thumbnail = ImageSpecField(source='avatar', processors=[ResizeToFill(200,200)], format='JPEG', options={'quality':60})

    def __str__(self):
		return str(self.username)+' - '+self.first_name+' '+self.last_name+' "'+self.description+'"'



class Post(models.Model):
	id_post = models.AutoField(primary_key=True)
	title = models.CharField(max_length=200, null=True)
	content = models.TextField(blank=True, null=True)
	source = models.CharField(max_length=200, null=True, unique=True)
	POST_STATE = (
        (1, 'Posted'),
        (2, 'Draft'),
        (3, 'Dumped')
    )
	state = models.IntegerField(choices=POST_STATE,default=2)
	site = models.CharField(max_length=100, null=True)
	id_article = models.CharField(max_length=100, null=True)
	description = models.TextField(blank=True, null=True)
	# tags = models.TextField(blank=True, null=True)
	# category = models.CharField(max_length=100, null=True)
	publishdate = models.CharField(max_length=100, null=True)
	image= models.ImageField(blank=True, null=True)
	created_at = models.DateTimeField(null=True)
	# created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	timestate = 3
	# slug = model.SLugField(default='', blank=True)
	image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(250,125)], format='JPEG', options={'quality':100})
	viewed = models.IntegerField(default=0)
	author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)

	def tagsplit(self):
		return Post_tag.objects.filter(post=self)

	def categorysplit(self):

		return Post_category.objects.filter(post=self)

	def titleslug(self):
		return slugify(self.title)

	def timehuman(self):
		result= self.created_at
		if (timezone.now()-self.created_at).days==0:
			result = naturaltime(self.created_at)
		elif (timezone.now()-self.created_at).days==1:
			result = naturalday(self.created_at)
		return result

	def content2(self):
		soupz = BeautifulSoup(self.content, 'html.parser')
		return soupz.text

	def content3(self):
		# soupz = BeautifulSoup(self.content, 'html.parser')
		tags = Tag.objects.filter(post_tag__post=self)
		konten=self.content
		for tagz in tags:
			soupz = BeautifulSoup(konten, 'html.parser')
			for p in soupz.findAll('p'):
				for te in p.findAll(text=True,recursive=False):
					# print(tagz.tag+' - '+str(te))
					fixed_text= str(te)
					fixed_text = fixed_text.replace(tagz.tag.upper(), tagz.tag).replace(tagz.tag.title(), tagz.tag).replace(tagz.tag, '<a href="'+reverse('tag', args=[slugify(tagz.tag)])+'"> '+tagz.tag+' </a>')
					newp = BeautifulSoup(fixed_text, 'html.parser')
					te.replace_with(newp)
			konten = str(soupz)

		# cats = Category.objects.filter(post_category__post=self)
		# for catz in cats:
		# 	soupz = BeautifulSoup(konten, 'html.parser')
		# 	for p in soupz.findAll('p'):
		# 		for te in p.findAll(text=True,recursive=False):
		# 			print(catz.category+' - '+str(te))
		# 			fixed_text= str(te)
		# 			fixed_text = fixed_text.replace(catz.category.upper(), catz.category).replace(catz.category.title(),catz.category).replace(catz.category, '<a href="'+reverse('category', args=[slugify(catz.category)])+'"> '+catz.category+' </a>')
		# 			newp = BeautifulSoup(fixed_text, 'html.parser')
		# 			te.replace_with(newp)
		# 	konten = str(soupz)
		return str(soupz)

	def get_absolute_url(self):
		return "/artikel/%i/%s/" % (self.id_post, slugify(self.title))

	def __str__(self):
		return self.title

class Quote(models.Model):
	id_quote = models.AutoField(primary_key=True)
	quote = models.TextField(blank=True, null=True)
	user= models.ForeignKey(User, on_delete=models.SET_NULL,null=True)

	def __str__(self):
		return self.quote

class Photo(models.Model):
	id_photo = models.AutoField(primary_key=True)
	id_post = models.IntegerField(blank=True, null=True)
	photo = models.ImageField(upload_to='post/')
	source = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.photo.url

class Topic(models.Model):
	id_topic= models.AutoField(primary_key=True)
	topic = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id_topic)+' - '+self.topic

class Site(models.Model):
	id_site= models.AutoField(primary_key=True)
	site = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id_site)+' - '+self.site

class Topic_site(models.Model):
	id_topic_site = models.AutoField(primary_key=True)
	topic= models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
	site = models.ForeignKey(Site, on_delete=models.SET_NULL,null=True)
	url= models.CharField(max_length=500, null=True)

	# POST_STATE = (
 #        (86400, '1 day (86400s)'),
 #        (43200, '12 hours (43200s)'),
 #        (21600, '6 hours (21600s)'),
 #        (10800, '3 hours (10800s)'),
 #        (3600, '1 hour (3600s)'),
 #        (1800, '30 minutes (1800s)'),
 #        (900, '15 minutes (900s)'),
 #        (300, '5 minutes (300s)'),
 #        (60, '1 minutes (60s)'),
 #    )
	# visitevery = models.IntegerField(choices=POST_STATE,default=86400)

	def __str__(self):
		return str(self.id_topic_site)+' - ['+str(self.topic.topic)+']['+str(self.site.site)+']'

	class Meta:
		unique_together = ('topic', 'site',)

class Category(models.Model):
	id_category = models.AutoField(primary_key=True)
	category = models.CharField(max_length=100, null=True)

	def get_absolute_url(self):
		return "/category/%s/" % (slugify(self.category))

class Tag(models.Model):
	id_tag = models.AutoField(primary_key=True)
	tag = models.CharField(max_length=100, null=True)

	def get_absolute_url(self):
		return "/tag/%s/" % (slugify(self.tag))

class Post_category(models.Model):
	id_post_category = models.AutoField(primary_key=True)
	category= models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
	post= models.ForeignKey(Post, on_delete=models.SET_NULL,null=True)

class Post_tag(models.Model):
	id_post_tag = models.AutoField(primary_key=True)
	tag= models.ForeignKey(Tag, on_delete=models.SET_NULL,null=True)
	post= models.ForeignKey(Post, on_delete=models.SET_NULL,null=True)


