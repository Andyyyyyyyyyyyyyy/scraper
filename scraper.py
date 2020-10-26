from bs4 import BeautifulSoup
import lxml
import requests


# cnbc.com x
# Bloomberg.com x
# senate.gov x
# businessinsider.com x
# cnn.com x
# foxbusiness.com x
# usatoday.com x
# washingtonpost.com x
# wsj.com x
# politico.com x
# Forbes.com x
# cbsnews.com x
# twitter.com

err_msg = "[ERROR]"

def scraper(url, tag, class_):
        site = url
        source = requests.get(site).text
        soup = BeautifulSoup(source, "lxml")
        headline = soup.find(tag, class_=class_).text
        return headline


def cnbc(url):
    headline = ""
    try:
        headline = scraper(url, "h1", "ArticleHeader-headline")
    except AttributeError:
        headline = scraper(url, "h1", "LiveBlogHeader-headline")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline


def bloomberg(url): # INFO: This will be blocked by a paywall most of the time
    headline = ""
    try:
        headline = scraper(url, "h1", "lede-text-v2__hed")
    except AttributeError:
        print("[ERROR] Unable to grab headline for Bloomberg, this is probably due to being blocked by the paywall")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def businessinsider(url):
    headline = ""
    try:
        headline = scraper(url, "h1", "post-headline")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def cnn(url):
    headline = ""
    try:
        headline = scraper(url, "h1", "pg-headline")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def foxbusiness(url):
    headline = ""
    try:
        headline = scraper(url, "h1", "headline")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def usatoday(url):
    headline = ""
    try:
        headline = scraper(url, "h1", "display-2")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def washingtonpost(url): # INFO: paywall!
    headline = ""
    try:
        headline = scraper(url, "h1", "font--headline balanced-headline pb-md")
    except AttributeError:
        print(f"[ERROR] Unable to grab headline from WashingtonPost.com, this is probably due to a paywall.")

    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def wsj(url): # INFO: doesnt work because website is loaded using javascript
    headline = ""
    try:
        headline = scraper(url, "h1", "wsj-article-headline")
    except AttributeError:
        print(f"[ERROR] Unable to grab headline from WSJ.com. (NoneType Error)")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def politico(url):
    headline = ""
    try:
        headline = scraper(url, "h2", "headline")
        if headline is None: # INFO: probably a newsletter type page
            site = url
            source = requests.get(site).text
            soup = BeautifulSoup(source, "lxml")
            headline = soup.find("meta", itemprop="headline").get("content")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def forbes(url):
    headline = ""
    try:
        headline = scraper(url, "h1", "fs-headline speakable-headline font-base font-size")
    except AttributeError:
        print(f"[ERROR] Unable to grab headline from Forbes.com. (NoneType Error)")
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline

def cbs(url):
    headline = ""
    try:
        headline = scraper(url, "h1", "content__title")
    except AttributeError: # probably a CBS This Morning Article
        site = url
        source = requests.get(site).text
        soup = BeautifulSoup(source, "lxml")
        headline = soup.find("h1", itemprop="headline").text
    except Exception as e:
        print(f"{err_msg} {e}")
    return headline
