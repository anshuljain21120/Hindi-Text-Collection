from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
def getSoup(url):
    try:
        html = requests.get(url, headers={'User-Agent':str(UserAgent().chrome)}).text
    except:
        html = "<html></html>"
    return BeautifulSoup(html, 'html.parser')
def getPages(url, uLimit=12000, eCount=5):
    url = "https://www.jagran.com"
    cErrorCount = 0
    pages = set()
    for a in getSoup(url).find("div", attrs = {'class' : 'MainLMenu tab', 'id' : "mainNav"}).find_all('a'):
        if len(a['href'])>2 and a['href'][0] == '/':
            try:
                for a0 in getSoup(url+str(a['href'])).find("div", attrs = {'class' : 'newsFJagran'}).find_all('a'):
                    pages.add(url+str(a0['href']))
                for i in range(2, uLimit):
                    header = str(a['href'])[:-5]+'-page'+str(i)+".html"
                    for ai in getSoup(url+header).find("div", attrs = {'class' : 'newsFJagran'}).find_all('a'):
                        pages.add(url+str(ai['href']))
            except:
                for a0 in getSoup(url+str(a['href'])).find_all("a", attrs = {'class' : 'aarPadhe'}):
                    try:
                        for a1 in getSoup(url+str(a0['href'])).find("div", attrs = {'class' : 'newsFJagran'}).find_all('a'):
                            pages.add(url+str(a1['href']))
                        for i in range(2, uLimit):
                            header = str(a0['href'])[:-5]+'-page'+str(i)+".html"
                            for ai in getSoup(url+header).find("div", attrs = {'class' : 'newsFJagran'}).find_all('a'):
                                pages.add(url+str(ai['href']))
                    except:
                        cErrorCount += 1
                        if cErrorCount >= eLimit:
                            break
    return pages
def getText(links):
    textData = set()
    for i in links:
        for p in getSoup(i).find_all('p'):
            textData.add(p.text)
    return textData