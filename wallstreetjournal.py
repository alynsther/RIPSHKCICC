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


index_of_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
index_of_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# #soup = BeautifulSoup(urllib2.urlopen('http://www.businessweek.com/archive/2009-01/bbg/day1.html').read())
# for year in range (2009, 2010):
# 	for month in range (11, 12):
# 		for day in range(1, index_of_days[month]):
# 			#http://www.wsj.com/public/page/archive-2015-7-14.html
# 			soup = BeautifulSoup(urllib2.urlopen('http://www.wsj.com/public/page/archive-' + str(year)+ '-' +str((month+1)) + '-' + str(day)+'.html').read())
# 			articles = soup.select('#archivedArticles ul li h2 a')
# 			links = [a['href'] for a in articles]
# 			for l in links:
# 				soup2 = BeautifulSoup(urllib2.urlopen(l))

# 				# try to find the subscription tag w/link, if found continue
# 				if soup2.select('.wsj-snippet-login'):
# 					continue

# 				article = soup2.select('#article_sector #wsj-article-wrap')[0]
# 				datestring = article.select('time')[0].text
# 				datetime = parse(datestring.strip().replace('Updated', ''))
# 				paragraphs = article.select('p')
# 				text = '\n\n'.join([p.text for p in paragraphs])


first_date = datetime(2009, 1, 1)
delta = timedelta(days=1)
date = first_date
last_date = datetime(2010, 1, 1)
while date < last_date:
	# do things 
	date += delta
	print date.month


def process(index, procs):
	i = 0
	while asdasd:
		if i % procs != index:
			continue




