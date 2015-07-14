import urllib2
import urllib
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import html2text
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# #soup = BeautifulSoup(urllib2.urlopen('http://www.businessweek.com/archive/2009-01/bbg/day1.html').read())

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

#soup = BeautifulSoup(urllib2.urlopen('http://www.businessweek.com/archive/2009-01/bbg/day1.html').read())
for year in range (2009, 2010):
	for month in range (0, 12):
		for day in range(1, index_of_days[month]+1):
			urllib.urlretrieve('http://www.businessweek.com/archive/' + str(year)+ '-' +str((month+1)).zfill(2)+'/bbg/day' + str(day)+'.html', "foobar.html")
			html = open("foobar.html").read()
			s = html2text.html2text(html)
			starting_search = s.find("#### " + index_of_months[month]  +" " + str(day).zfill(2) + ", " + str(year))
			starting_place = s.find("[", starting_search)
			ending_place = s.find("]", starting_search)
			while(ending_place < s.find("Terms of Service")):
				print(s[starting_place+1 :ending_place])
				f = open("bloomberg_" + str(year) + "_" + str(month+1) + "_"+ str(day) + ".txt", "a")
				f.write(s[starting_place+1:ending_place])
				f.write('\n')
				f.close
				starting_search = ending_place + 1
				starting_place = s.find("[", starting_search)
				ending_place = s.find("]", starting_search)
				

				