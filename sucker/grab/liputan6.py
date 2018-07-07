from __future__ import unicode_literals
from sucker.grab import grabhelper as gh

from sucker.models import Post
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse

def visit():
	d={}
	d['grabbed']=0
	url='https://www.liputan6.com/sitemap_post.xml'
	page = requests.get(url)
	soupz = BeautifulSoup(page.content, 'xml')
	for a in soupz.findAll("loc"):
		post_count = Post.objects.filter(source=a.string).count()
		if post_count==0:
			d['grabbed']+=artikel(a.string)
	return d


from urlparse import urlparse
def visitTopic(url,limit):
	d={}
	d['grabbed']=0
	# url= 'https://www.liputan6.com/lifestyle'
	page = requests.get(url)
	soupz = BeautifulSoup(page.content, 'html.parser')
	for a in soupz.find("article", attrs={'main'}).findAll('a'):
		# print(a['href'])
		if d['grabbed']>=limit:
			break
		if 'liputan6.com' in str(urlparse(a['href']).hostname) and '/read/' in a['href'] and '/top-' not in a['href'] and '/video-' not in a['href'] and '/foto-' not in a['href'] :
			if not Post.objects.filter(source=a['href'].split('?',1)[0]).count():
				d['grabbed']+=artikel(a['href'].rsplit('?', 1)[0])['status']
		
	d['url']=url
	d['limit']=limit
	return d


def artikel(url):
	result=0
	d={}
	d['status']=0
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		d['url']=url
		uParse = urlparse(url)
		idd = str(uParse.path).split('/')[3]
		d['id_article']=idd
		d['title']=soup.find("meta",  property="og:title")['content']
		d['description']= soup.find("meta",  property="og:description")['content']
		d['image']= soup.find("meta",  property="og:image")['content']
		d['tags']= soup.find("meta",  attrs={'name':'keywords'})['content']
		d['publishdate']= soup.find("time")['datetime']
		d['category']= soup.find("meta",  attrs={'name':'adx:sections'})['content']
		d['site']='Liputan 6'
		# print(d)
		content = soup.find("div",  attrs={'class':'article-content-body_with-aside'})
		for t in content.findAll(text=True):
			newtext = t.replace("&nbsp", "").encode("ascii", "ignore").strip('\r\n')
			t.replace_with(newtext)
		wedo=BeautifulSoup('<div class="content"></div>', 'html.parser')
		js_instagram=0
		for secpar in content.find_all('div', {'class':'article-content-body__item-page'},recursive=False):
			dtitle=BeautifulSoup('<p><strong>'+secpar['data-title']+'<strong></p>', 'html.parser')
			wedo.div.append(dtitle)
			# print(secpar['class'])
			for sec in secpar.find_all('div',recursive=False):
				# print(sec['class'])
				for ele in  sec.findAll(['p', 'blockquote','figure','ul','img'],recursive=False):
					# print(ele.name)
					if ele.name == 'blockquote':
						if ele['class'][0] == 'instagram-media':
							js_instagram+=1
							wedo.div.append(ele)
					if ele.name=='ul':
			 			del ele.attrs
			 			wedo.div.append(ele)
			 		if ele.name=='p':
						for a in ele.findAll('a'):
							a.unwrap()
						# [x.extract() for x in content.findAll(['strong','b'])]
						# ele.b.decompose()
						# ele.strong.decompose()
						del ele.attrs
						wedo.div.append(ele)
					if ele.name == 'figure':
						img_src= ele['data-image']
						img_alt= ele['data-description']
						img_alt= ele.text
						newimg='<figure class="wp-caption aligncenter" jQuery><a href="'+img_src+'" class="popup_link"><img src="'+img_src+'" alt="'+img_alt+'"></a><figcaption class="wp-caption-text">'+img_alt+'</figcaption></figure>'
		 				figure=BeautifulSoup(newimg, 'html.parser')
		 				wedo.div.append(figure)
		if js_instagram:
			js=BeautifulSoup('<script async defer src="//www.instagram.com/embed.js"></script>', 'html.parser')
			wedo.div.append(js)
		d['content']= str(wedo)
		if gh.insert_to_db(d):
			d['status']=1
		print('Done: Liputan6')
	except Exception as e:
		d['status']=0
		print('Failed: Liputan6: '+str(e))
	return d
	
	