from __future__ import unicode_literals
from sucker.grab import grabhelper as gh

from sucker.models import Quote,User

import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
from django.db.models import Q
import random

def grabquote():
	result=0
	d={}
	d['status']=0
	try:
		url='https://karyapemuda.com/quotes-bijak/'
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		for t in soup.find_all(text=True):
			newtext = t.replace("&nbsp", "").encode("ascii", "ignore").strip('\r\n')
			t.replace_with(newtext)
		d['url']=url
		for p in soup.findAll("p", attrs={'style':'text-align: center;'}):
			if not Quote.objects.filter(quote=str(p.text).strip()):
				print(str(p.text))
				Quote(quote=str(p.text).strip()).save()

		users = User.objects.filter(Q(description='') | Q(description=None))
		quotes= Quote.objects.filter(user=None)
		print(users.count())
		print(quotes.count())
		for u in users:
			print('iterate')
			quo = quotes[random.randint(0,quotes.count()-1)]
			u.description= quo.quote
			u.save()
			quo.user=u
			quo.save()
			print('saved')
		d['status']=1
	except Exception as e:
		d['status']=0
		print('Failed: Quote: '+str(e))
	return d

