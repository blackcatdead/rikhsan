from __future__ import unicode_literals
from sucker.grab import grabhelper as gh

from sucker.models import Post
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
from time import sleep


def visit():
	d={}
	d['grabbed']=0
	url='https://kompas.com/'
	page = requests.get(url)
	soupz = BeautifulSoup(page.content, 'html.parser')
	# print(str(soupz))
	for a in soupz.findAll('a',  attrs={'class':'footer__menu__link'}):
		
		if a.string in ['News','Nasional','Regional','Megapolitan','Internasional','Sains','Edukasi','Olahraga','Bola','Tekno','Entertainment','Otomotif','Travel','Health','Lifestyle','Properti']:
			# print(a.string)
			page = requests.get(a['href'])
			soup = BeautifulSoup(page.content, 'html.parser')
			for artk in soup.findAll('div', attrs={'class':'article__asset'}):
				try:
					a=artk.find('a')
					if 'href' in a.attrs:
						link=artk.find('a')['href']
						# print('Grabbing: '+link)
						post_count = Post.objects.filter(source=link).count()
						if post_count==0:
							d['grabbed']+=artikel(link)
							# sleep(5)
				except Exception as e:
					print(e)
					
	return d

from urlparse import urlparse
def visitTopic(url,limit):
	d={}
	d['grabbed']=0
	# url= 'https://www.liputan6.com/lifestyle'
	page = requests.get(url)
	soupz = BeautifulSoup(page.content, 'html.parser')
	for a in soupz.find("div", attrs={'class':'col-bs10-7'}).findAll('a'):
		# print(a['href'])
		if d['grabbed']>=limit:
			break
		if 'kompas.com' in str(urlparse(a['href']).hostname) and '/read/' in a['href'] :
			# print(a['href'])
			if not Post.objects.filter(source=a['href'].split('?',1)[0]).count():
				print(a['href'])
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
		idd = str(uParse.path).split('/')[5]
		d['id_article']=idd
		d['title']=soup.find("h1",  attrs={'class':'read__title'}).text
		d['description']= soup.find("meta",  property="og:description")['content']
		# d['image']= soup.find("meta", property="og:image")['content']
		# print(d['image'])
		# d['image']= getrealimg(soup.find("meta",  property="og:image")['content'])
		# print(soup.find('div', attrs={'class':'photo'}))
		d['image']= soup.find('div', attrs={'class':'photo'}).find('img')['src']

		# d['tags']= soup.find("meta",  attrs={'name':'keywords'})['content']
		
		tagg=''
		
		for tta in soup.findAll("li", attrs={'class':'tag__article__item'}):
			# print(tta.text)
			tagg+= tta.text+','
		# print(tagg)
		d['tags']=tagg
		d['publishdate']= soup.find("meta",  attrs={'name':'content_PublishedDate'})['content']
		d['category']= soup.find("meta",  attrs={'name':'content_category'})['content']
		d['site']='Kompas'
		content=None
		if soup.findAll('div', attrs={'class':'read__text--content'}):
			content = soup.find("div",  attrs={'class':'read__text--content'})
		else:
			content = soup.find("div",  attrs={'class':'read__content'})
		

		for t in content.find_all(text=True):
			newtext = t.replace("&nbsp", "").encode("ascii", "ignore").strip('\r\n')
			t.replace_with(newtext)
		wedo=BeautifulSoup('<div class="content"></div>', 'html.parser')
		js_instagram=0
		js_youtube=0
		js_tweet=0
		for x in content.find_all(recursive=False):
			# print(x.name)
			# print(str(x))
			if x.name=='p' or x.name=='div':

				caritag = x.findAll(['div','iframe'],recursive=False)
				for dlm in caritag:
					if dlm.name == 'div':
						if 'photo' in dlm['class']:
							imgnya= dlm.find('img')
							captionnya= imgnya['alt']
							
							newimg='<figure class="wp-caption aligncenter" jQuery><a href="'+imgnya['src']+'" class="popup_link"><img src="'+imgnya['src']+'" alt="'+captionnya+'"></a><figcaption class="wp-caption-text">'+captionnya+'</figcaption></figure>'
							x=BeautifulSoup(newimg, 'html.parser')
							wedo.div.append(x)

						if 'photo-infographic' in dlm['class']:
							imgnya= dlm.find('img')
							captionnya= imgnya['data-title']
							
							newimg='<figure class="wp-caption aligncenter" jQuery><a href="'+imgnya['src']+'" class="popup_link"><img src="'+imgnya['src']+'" alt="'+captionnya+'"></a><figcaption class="wp-caption-text">'+captionnya+'</figcaption></figure>'
							x=BeautifulSoup(newimg, 'html.parser')
							wedo.div.append(x)

					if dlm.name == 'iframe':
						if 'youtube.com/embed' in dlm['src']:
							js_youtube+=1
							xx=BeautifulSoup('<iframe width="560" height="315" src="'+dlm['src']+'" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', 'html.parser')
							wedo.div.append(xx)
					# print(dlm.name)
					# if dlm.name:
					# 	print(dlm.text)
				if not caritag:
					for a in x.findAll('a', attrs={'class':'inner-link'}):
						a.unwrap()
					for st in x.findAll('strong'):
						if 'Baca juga:' in st.text or 'Baca Juga:' in st.text:
							st.extract()
					for br in x.findAll('br'):
						br.extract()
					for sc in x.findAll('script'):
						sc.extract()
					xx=BeautifulSoup('<p>'+x.text+'</p>', 'html.parser')
					# print(x.text)
					# del x.attrs
					wedo.div.append(xx)
				# if x.findAll('div'): 
				# 	divs= x.findAll('div')
				# 	for div in divs:
				# 		if 'photo' in div['class']:
				# 			print(div['class'])
				# 			imgnya= div.find('img')
				# 			captionnya= imgnya['alt']
							
				# 			newimg='<figure class="wp-caption aligncenter" jQuery><a href="'+imgnya['src']+'" class="popup_link"><img src="'+imgnya['src']+'" alt="'+captionnya+'"></a><figcaption class="wp-caption-text">'+captionnya+'</figcaption></figure>'
				# 			x=BeautifulSoup(newimg, 'html.parser')
				# 			wedo.div.append(x)
				# if x.findAll('a', attrs={'class':'inner-link'}):
				# 	for a in x.findAll('a', attrs={'class':'inner-link'}):
				# 		a.unwrap()
				# 	del x.attrs
				# 	for st in x.findAll('strong'):
				# 		if 'Baca juga:' in st.text:
				# 			st.extract()
				# 	for br in x.findAll('br'):
				# 		br.extract()
				# 	wedo.div.append(x)
				# 	# if 'Baca juga:' not in x.text and x.text is not '':
				# 	# 	wedo.div.append(x)
				# else:
				# 	del x.attrs
				# 	if x.text is not '':
				# 		wedo.div.append(x)
			if x.name== 'blockquote':
				print('blackquote')
				if x['class'][0] == 'instagram-media':
					js_instagram+=1
					wedo.div.append(x)
				if x['class'][0] == 'twitter-tweet':
					js_tweet+=1
					wedo.div.append(x)
			# if x.name== 'iframe':
			# 	if 'https://www.youtube.com/embed' in x['src']:
			# 		wedo.div.append(x)
		if js_instagram:
			js=BeautifulSoup('<script async defer src="//www.instagram.com/embed.js"></script>', 'html.parser')
			wedo.div.append(js)
		if js_tweet:
			js=BeautifulSoup('<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>', 'html.parser')
			wedo.div.append(js)
			
		d['content']= str(wedo)
		if gh.insert_to_db(d):
		  	d['status']=1
		print('Done: Kompas')
	except Exception as e:
	 	d['status']=0
	return d

def getrealimg(url):
	fina=""
	mustbesaved=[]
	save=0
	parsed= urlparse(str(url))
	fina = parsed.scheme+'://'+parsed.netloc
	for pa in reversed(parsed.path.split('/')):
		# print(pa)
		mustbesaved.append(pa)
		if pa == 'data':
			break

	for ms in reversed(mustbesaved):
		fina+='/'+ms
		# print(ms)
		
		# if not save:
		# 	# mustberemoved.append(pa)
		# 	parsed.remove(pa)
	# print(fina)

	return fina