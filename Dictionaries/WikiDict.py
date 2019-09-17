import urllib.request
from bs4 import BeautifulSoup
import ssl
import re
import pandas as pd

def getSoup(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        html = urllib.request.urlopen(str(url), context=ctx).read()
    except:
        return BeautifulSoup("<html></html>", "html.parser")
    return BeautifulSoup(html, "html.parser")

def isHindi(word):
    hindi = re.compile("[U00000000-U000FFFFF\u0000-\u0899\u0964-\u0971\u0980-\U000FFFFF u002D]")
    if hindi.sub(' ',word)==word:
        return True
    return False

def getWords(sorted=True):
    words = set()
    header = "https://hi.wiktionary.org"
    url = "/w/index.php?title=%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A5%87%E0%A4%B7:%E0%A4%B8%E0%A4%AD%E0%A5%80_%E0%A4%AA%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A0&from=%E0%A4%86"
    while(True):
        soup = getSoup(header + url)
        for li in soup.find('div', class_="mw-allpages-body").find_all('li'):
            word = li.find('a').text
            if len(word)<14 and len(word)>1 and isHindi(word):
                words.add(word)
        print("\r {:,} collected, still collecting...".format(len(words)), end="")
        if len(soup.find('div', class_="mw-allpages-nav").find_all('a'))==2:
            url = str(soup.find('div', class_="mw-allpages-nav").find_all('a')[1].get("href"))
        else:
            break
    print("\r {:,} collected, crawler closed succesfully.                 ".format(len(words)))
    if (sorted):
        words = list(words)
        words.sort()
        words = set(words)
    return words
