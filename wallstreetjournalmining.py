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
def processtextmine(index, procs):
	first_date = datetime(2010, 1, 1)
	delta = timedelta(days=1)
	date = first_date - delta
	last_date = datetime(2010, 12, 31)
	while date < last_date:
		date+= delta
		if date.month % procs != index:
			continue
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




