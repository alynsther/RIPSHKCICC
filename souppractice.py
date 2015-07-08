import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import httplib2


soup = BeautifulSoup(urllib2.urlopen('http://www.bloomberg.com/').read())
#print(soup)
for i in soup.findAll('time'):
        if i.has_attr('datetime'):
            print(i['datetime'])



#for i in soup.findAll('url'):
#	if i.has_attr('src'):
#		print(i['src'])

for i in soup.findAll('a'):
	if i.has_attr('href'):
		s = "www.bloomberg.com/" + i['href']
		print(i.title)
			 # goodstring = True
			 # for i in range(len(s)):
				# if s[i:i+4] == "http":
			 # 		goodstring = False
			 #if(goodstring):
		print(s)



			
#s = '''<time class="jlist_date_image" datetime="2015-04-02 14:30:12">Idag <span class="list_date">14:30</span></time>'''
#soup = BeautifulSoup(s)
#for i in soup.findAll('time'):
 #       if i.has_attr('datetime'):
  #          print(i['datetime'])

