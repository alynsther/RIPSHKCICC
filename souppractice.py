import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import httplib2

#open the article
soup = BeautifulSoup(urllib2.urlopen('http://www.bloomberg.com/').read())
#print(soup)
#find things with time tag and attribute 'datetime.' doesn't work for all articles
for i in soup.findAll('time'):
        if i.has_attr('datetime'):
            print(i['datetime'])



#for i in soup.findAll('url'):
#	if i.has_attr('src'):
#		print(i['src'])


#finds all the links
list_of_hyperlinks = ["www.bloomberg.com"]
for i in soup.findAll('a'):
	if i.has_attr('href'):
		s = "www.bloomberg.com/" + i['href']
		goodstring = False
		 #cleans up the useless strings
		for i in range(len(s)):
			if s[i:i+4] == "news":
				goodstring = True
		if(goodstring):
			list_of_hyperlinks.append(s)


print(set(list_of_hyperlinks))

			
#s = '''<time class="jlist_date_image" datetime="2015-04-02 14:30:12">Idag <span class="list_date">14:30</span></time>'''
#soup = BeautifulSoup(s)
#for i in soup.findAll('time'):
 #       if i.has_attr('datetime'):
  #          print(i['datetime'])

