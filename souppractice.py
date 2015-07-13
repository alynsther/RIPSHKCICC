import urllib2
import urllib
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import html2text
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#open the article
soup = BeautifulSoup(urllib2.urlopen('http://www.wsj.com/public/page/archive-2015-5-13.html').read())
#print(soup)
#find things with time tag and attribute 'datetime.' doesn't work for all articles
# for i in soup.findAll('time'):
#         if i.has_attr('datetime'):
#             print(i['datetime'])






#finds all the links
list_of_hyperlinks = ["google.com"]
for i in soup.findAll('a'):
	if i.has_attr('href'):
		s =  i['href']
		goodstring = False
		 #cleans up the useless strings
		for i in range(len(s)):
			if s[i:i+8] == "articles":
				goodstring = True
		if(goodstring):
			list_of_hyperlinks.append(s)


print(list_of_hyperlinks)
print(len(list_of_hyperlinks))
for i in range(1, len(list_of_hyperlinks)):
	urllib.urlretrieve(list_of_hyperlinks[i], "foobar.html")
	html = open("foobar.html").read()
	s = html2text.html2text(html)
	starting_place = s.find("Updated")
	ending_place = s.find("To Read the Full Story", starting_place)
	if starting_place != -1 and ending_place !=1:
		print(s[starting_place:ending_place])
		f = open("test513.txt", "a")
		f.write(s[starting_place:ending_place])
		f.close



			
#s = '''<time class="jlist_date_image" datetime="2015-04-02 14:30:12">Idag <span class="list_date">14:30</span></time>'''
#soup = BeautifulSoup(s)
#for i in soup.findAll('time'):
 #       if i.has_attr('datetime'):
  #          print(i['datetime'])