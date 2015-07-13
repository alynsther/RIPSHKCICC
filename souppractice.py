import urllib2
import urllib
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import html2text
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#open the article
soup = BeautifulSoup(urllib2.urlopen('http://www.businessweek.com/archive/2015-02/bbg.html').read())
#print(soup)
#find things with time tag and attribute 'datetime.' doesn't work for all articles
for i in soup.findAll('time'):
        if i.has_attr('datetime'):
            print(i['datetime'])






# #finds all the links
# list_of_hyperlinks = ["www.bloomberg.com"]
# for i in soup.findAll('a'):
# 	if i.has_attr('href'):
# 		s =  i['href']
# 		# s =  "WWW.BLOOMBERG.COM" + i['href']
# 		goodstring = False
# 		 #cleans up the useless strings
# 		for i in range(len(s)):
# 			if s[i:i+4] == "news":
# 				goodstring = True
# 		if(goodstring):
# 			list_of_hyperlinks.append(s)


# print(set(list_of_hyperlinks))

urllib.urlretrieve("http://www.wsj.com/articles/provocateur-j-j-brine-stirs-up-new-york-art-scene-1431465492", "foobar.html")
html = open("foobar.html").read()
s = html2text.html2text(html)
print(s)

#bug: regardless of character, prints the same results. 
starting_place = s.find("COMMENTS")
ending_place = s.find("**Write to", starting_place)
print(starting_place)
print(ending_place)

print(s[starting_place:ending_place])


f = open("test.txt", "w")
f.write(s[starting_place:ending_place])



			
#s = '''<time class="jlist_date_image" datetime="2015-04-02 14:30:12">Idag <span class="list_date">14:30</span></time>'''
#soup = BeautifulSoup(s)
#for i in soup.findAll('time'):
 #       if i.has_attr('datetime'):
  #          print(i['datetime'])