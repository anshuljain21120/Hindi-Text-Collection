import urllib.request
# This Crawler is only for site https://aajtak.intoday.in/ 

from bs4 import BeautifulSoup
import ssl
def getSoup(url):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	try:		
		html = urllib.request.urlopen(str(url), context=ctx).read()
	except:
		return BeautifulSoup("<html></html>", "html.parser")
	return BeautifulSoup(html, "html.parser")

def getPages(uLimit=12000, eLimit=5):
	url = "https://aajtak.intoday.in"
	pages = set()
	try:
		for a in getSoup(url).find('nav').find_all('a'):
			for i in range(uLimit):
				try:
					cErrorCount = 0
					for a in getSoup(url+str(a['href'])+"/"+str(i)).find_all('a', class_='photoHitContainer1'):
						pages.add(url+str(a['href']))
						print("\r {0:,} links pulled still fetching...".format(len(pages)), end="")
				except:
					cErrorCount += 1
					if cErrorCount >= eLimit:
						break
	except:
		print("Network error!")
	print("\r Total {:,} links fetched.             ".format(len(pages)))
	return pages

def getText(links):
	textData = set()
	for i in links:
	    for p in getSoup(i).find_all('p'):
	        textData.add(p.text)
	return textData
