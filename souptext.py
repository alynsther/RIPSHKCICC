import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import httplib2


soup = BeautifulSoup(urllib2.urlopen('http://www.bloomberg.com/news/articles/2015-07-08/china-s-market-rescue-makes-matters-worse-as-prices-lose-meaning').read())

texts = soup.findAll(text=True)
visible_texts = filter(visible, texts)
print(visible_texts)


#print(soup.get_text())