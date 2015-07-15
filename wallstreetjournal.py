import urllib2
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


first_date = datetime(2009, 7, 8)
delta = timedelta(days=1)
date = first_date - delta
last_date = datetime(2009, 7, 10)
#soup = BeautifulSoup(urllib2.urlopen('http://www.businessweek.com/archive/2009-01/bbg/day1.html').read())
while date < last_date:
	date+= delta
	print('http://www.wsj.com/public/page/archive-' + str(date.year)+ '-' +str((date.month)) + '-' + str(date.day)+'.html')
	soup = BeautifulSoup(urllib2.urlopen('http://www.wsj.com/public/page/archive-' + str(date.year)+ '-' +str((date.month)) + '-' + str(date.day)+'.html').read())
	articles = soup.select('#archivedArticles ul li h2 a')
	links = [a['href'] for a in articles]
	linkindex = 0
	print(links)
	for l in links:
		soup2 = BeautifulSoup(urllib2.urlopen(l))

		# try to find the subscription tag w/link, if found continue
		if soup2.select('.wsj-snippet-login'):
			continue

		article = soup2.select('#article_sector #wsj-article-wrap')[0]
		datestring = article.select('time')[0].text
		datetime = parse(datestring.strip().replace('Updated', ''))
		paragraphs = article.select('p')
		text = '\n\n'.join([p.text for p in paragraphs])
		print(text)
		f = open("wsj" + str(date.year)+ '_' +str((date.month)) + '_' + str(date.day) + "_fileno_" + str(linkindex) + ".txt", "a")
		f.write(text)
		f.close
		date += delta
		linkindex+=1




def process(index, procs):
	i = 0
	while asdasd:
		if i % procs != index:
			continue




