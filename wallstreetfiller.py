from urllib2 import urlopen,HTTPError
import urllib
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import html2text
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
from dateutil.parser import parse
from datetime import datetime, timedelta


#soup = BeautifulSoup(urllib2.urlopen('http://www.businessweek.com/archive/2009-01/bbg/day1.html').read())

# urllib.urlretrieve('http://www.businessweek.com/archive/2009-01/bbg/day2.html', "foobar.html")
# html = open("foobar.html").read()
# s = html2text.html2text(html)

# starting_search = s.find("#### January 02, 2009")
# starting_place = s.find("[", starting_search)
# ending_place = s.find("]", starting_search)
# while(ending_place < s.find("Terms of Service")):
# 	print(s[starting_place+1 :ending_place])
# 	starting_search = ending_place + 1
# 	starting_place = s.find("[", starting_search)
# 	ending_place = s.find("]", starting_search)
				
	#s = '''<time class="jlist_date_image" datetime="2015-04-02 14:30:12">Idag <span class="list_date">14:30</span></time>'''
	#soup = BeautifulSoup(s)
	#for i in soup.findAll('time'):
	 #       if i.has_attr('datetime'):
	  #          print(i['datetime'])




#index should maybe be date.month and do 4 or 6 at once
#run this with index 0 1 2 and 3
#procs is the number of simultaneous processes to run
#enter 0, 1 in order to just do it all with one process
#error with 2012-1-14 key error href. maybe it just doesn't want to print all links?

daterange = [datetime(2010, 3, 31),
datetime(2010, 3, 31),
datetime(2010, 5, 20),
datetime(2011, 2, 3),
datetime(2011, 2, 6),
datetime(2011, 2, 8),
datetime(2011, 2, 9),
datetime(2011, 2, 11),
datetime(2011, 2, 13),
datetime(2011, 2, 16),
datetime(2011, 2, 17),
datetime(2011, 2, 19),
datetime(2011, 2, 22),
datetime(2011, 2, 23),
datetime(2011, 2, 24),
datetime(2011, 2, 25),
datetime(2011, 2, 28),
datetime(2011, 3, 29),
datetime(2011, 3, 30),
datetime(2011, 4, 3),
datetime(2011, 4, 7),
datetime(2011, 4, 11),
datetime(2011, 4, 15),
datetime(2011, 4, 17),
datetime(2011, 4, 18),
datetime(2011, 4, 19),
datetime(2011, 4, 22),
datetime(2011, 4, 23),
datetime(2011, 4, 26),
datetime(2011, 5, 22),
datetime(2011, 5, 27),
datetime(2011, 5, 28),
datetime(2011, 5, 29),
datetime(2011, 5, 30),
datetime(2011, 6, 1),
datetime(2011, 6, 2),
datetime(2011, 6, 6),
datetime(2011, 6, 11),
datetime(2011, 6, 12),
datetime(2011, 6, 13),
datetime(2011, 6, 15),
datetime(2011, 6, 17),
datetime(2011, 6, 21),
datetime(2011, 6, 24),
datetime(2011, 6, 30),
datetime(2011, 7, 1),
datetime(2011, 7, 2),
datetime(2011, 7, 3),
datetime(2011, 7, 8),
datetime(2011, 7, 13),
datetime(2011, 7, 15),
datetime(2011, 7, 17),
datetime(2011, 7, 18),
datetime(2011, 7, 20),
datetime(2011, 7, 21),
datetime(2011, 7, 23),
datetime(2011, 7, 24),
datetime(2011, 7, 27),
datetime(2011, 7, 28),
datetime(2011, 7, 30),
datetime(2011, 8, 5),
datetime(2011, 8, 6),
datetime(2011, 8, 7),
datetime(2011, 8, 8),
datetime(2011, 8, 9),
datetime(2011, 8, 12),
datetime(2011, 8, 13),
datetime(2011, 8, 15),
datetime(2011, 8, 16),
datetime(2011, 8, 17),
datetime(2011, 8, 18),
datetime(2011, 8, 19),
datetime(2011, 8, 21),
datetime(2011, 8, 22),
datetime(2011, 8, 23),
datetime(2011, 8, 24),
datetime(2011, 8, 25),
datetime(2011, 8, 26),
datetime(2011, 8, 27),
datetime(2011, 8, 28),
datetime(2011, 8, 29),
datetime(2011, 8, 31),
datetime(2011, 9, 1),
datetime(2011, 9, 3),
datetime(2011, 9, 4),
datetime(2011, 9, 6),
datetime(2011, 9, 8),
datetime(2011, 9, 9),
datetime(2011, 9, 11),
datetime(2011, 9, 13),
datetime(2011, 9, 14),
datetime(2011, 9, 15),
datetime(2011, 9, 17),
datetime(2011, 9, 20),
datetime(2011, 9, 21),
datetime(2011, 9, 22),
datetime(2011, 9, 23),
datetime(2011, 9, 25),
datetime(2011, 9, 28),
datetime(2011, 9, 29),
datetime(2011, 10, 2),
datetime(2011, 10, 5),
datetime(2011, 10, 7),
datetime(2011, 10, 10),
datetime(2011, 10, 11),
datetime(2011, 10, 13),
datetime(2011, 10, 14),
datetime(2011, 10, 15),
datetime(2011, 10, 18),
datetime(2011, 10, 21),
datetime(2011, 10, 22),
datetime(2011, 10, 24),
datetime(2011, 10, 26),
datetime(2011, 10, 30),
datetime(2011, 11, 6),
datetime(2011, 11, 7),
datetime(2011, 11, 8),
datetime(2011, 11, 9),
datetime(2011, 11, 10),
datetime(2011, 11, 11),
datetime(2011, 11, 12),
datetime(2011, 11, 13),
datetime(2011, 11, 14),
datetime(2011, 11, 15),
datetime(2011, 11, 17),
datetime(2011, 11, 18),
datetime(2011, 11, 19),
datetime(2011, 11, 23),
datetime(2011, 11, 25),
datetime(2011, 11, 27),
datetime(2011, 11, 30),
datetime(2011, 12, 2),
datetime(2011, 12, 5),
datetime(2011, 12, 7),
datetime(2011, 12, 13),
datetime(2011, 12, 17),
datetime(2011, 12, 21),
datetime(2011, 12, 22),
datetime(2011, 12, 27),
datetime(2011, 12, 28),
datetime(2011, 12, 29),
datetime(2011, 12, 30),
datetime(2012, 1, 14),
datetime(2012, 1, 24),
datetime(2012, 4, 13),
datetime(2012, 5, 24),
datetime(2012, 6, 30),
datetime(2012, 7, 6),
datetime(2012, 7, 12),
datetime(2012, 7, 23),
datetime(2012, 9, 7),
datetime(2012, 12, 7),
datetime(2013, 2, 8),
datetime(2013, 3, 26),
datetime(2013, 12, 12),
datetime(2014, 5, 3),
datetime(2015, 2, 9),
datetime(2015, 2, 14),
datetime(2015, 4, 12),
datetime(2015, 4, 14),
datetime(2015, 4, 18),
datetime(2015, 5, 9),
]
print(daterange[0])
for date in daterange:
	print('http://www.wsj.com/public/page/archive-' + str(date.year)+ '-' +str((date.month)) + '-' + str(date.day)+'.html')
	soup = BeautifulSoup(urlopen('http://www.wsj.com/public/page/archive-' + str(date.year)+ '-' +str((date.month)) + '-' + str(date.day)+'.html').read())
	articles = soup.select('#archivedArticles ul li h2 a')
	try:
		links = [a['href'] for a in articles]
	except:
		g = open("wsj" + str(date.year)+ '_' +str((date.month)) + '_' + str(date.day) + "_error.txt", "a")
		print('Unexpected error being logged')
		g.write("Error on date link:" + str(date)+".txt")
		g.close
		continue
	linkindex = 0
	print(links)
	for l in links:
		try:
			soup2 = BeautifulSoup(urlopen(l))
		except (HTTPError, ValueError, KeyError):
			print "Oops! Page broken"
			continue
		except:
			f = open("wsj" + str(date.year)+ '_' +str((date.month)) + '_' + str(date.day) + "_error_no_" + str(linkindex) + ".txt", "a")
			print('Unexpected error being logged')
			f.write("Error after link:" + str(date))
			continue
		#look for missing dates like all of february 2011
		# try to find the subscription tag w/link, if found continue
		if soup2.select('.wsj-snippet-login'):
			continue
		if soup2.select('#article_sector #wsj-article-wrap'):
			article = soup2.select('#article_sector #wsj-article-wrap')[0]
			paragraphs = article.select('p')
			text = '\n\n'.join([p.text for p in paragraphs])
			print(text.encode('ascii', "ignore"))
			f = open("wsj" + str(date.year)+ '_' +str((date.month)) + '_' + str(date.day) + "_fileno_" + str(linkindex) + ".txt", "w")
			f.write(text.encode('ascii', "ignore"))
			f.close
			linkindex+=1




