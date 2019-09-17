import urllib.request
from bs4 import BeautifulSoup
import ssl
import requests
import re
def getSoup(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        html = urllib.request.urlopen(str(url), context=ctx).read()
    except:
        return BeautifulSoup("<html></html>", "html.parser")
    return BeautifulSoup(html, "html.parser")
def getPages():
    pages = set()
    header = "https://hi.wikipedia.org"
    url = "/wiki/%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A5%87%E0%A4%B7:%E0%A4%B8%E0%A4%AD%E0%A5%80_%E0%A4%AA%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A0/%E0%A4%85"
    while(True):
        soup = getSoup(header + url)
        for li in soup.find('div', class_="mw-allpages-body").find_all('li'):
            pages.add(li.find('a').get('href'))
        print("\r {:,} collected, still collecting...".format(len(pages)), end="")
        if len(soup.find('div', class_="mw-allpages-nav").find_all('a'))==2:
            url = str(soup.find('div', class_="mw-allpages-nav").find_all('a')[1].get("href"))
        else:
            break
    print("\r {:,} collected, crawler closed succesfully.                 ".format(len(pages)))
    return pages
def convertNumerics(text):
    text = re.sub('0', u'\u0966', text)
    text = re.sub('1', u'\u0967', text)
    text = re.sub('2', u'\u0968', text)
    text = re.sub('3', u'\u0969', text)
    text = re.sub('4', u'\u096A', text)
    text = re.sub('5', u'\u096B', text)
    text = re.sub('6', u'\u096C', text)
    text = re.sub('7', u'\u096D', text)
    text = re.sub('8', u'\u096E', text)
    return re.sub('9', u'\u096F', text)
def getHindi(text):
    re.compile("[\u00A0-\u00FFu0900-u0971]").sub(' ',convertNumerics(text))
    text = re.sub(r'[\.,:\'\/"]+\s*[\.,:\'\/"0-9]*', ' ', re.sub(r'[a-zA-Z]', '', text))
    return re.sub(r'\s+', ' ', re.sub(r'\(\s*\)', ' ', re.sub(r'\[.*\s*\]', ' ', text) ) ).strip()
def getText(header, pages):
    text = set()
    pages = set(pages)
    try:
        for url in pages:
            for p in getSoup(header + url).find('div', class_="mw-parser-output").find_all('p'):
                text.add(getHindi(str(p.text)))
            print("\r {:,} paragraphs collected, still collecting...".format(len(text)), end="")
        print("\r {:,} paragraphs collected, crawler closed succesfully.                 ".format(len(text)))
    except:
        print("\r {:,} paragraphs collected, crawler closed unexpectedly.                 ".format(len(text)))
        pass
    return text
