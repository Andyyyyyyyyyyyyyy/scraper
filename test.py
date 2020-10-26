from bs4 import BeautifulSoup
import lxml
import requests
import re
import csv
from urllib.parse import urlparse


def scan(string):
    regex = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)"
    url = re.findall(regex,string)
    return [x for x in url]




link = scan("https://www.foxbusiness.com/economy/sept-new-home-sales-fall-3-5-after-strong-summer-season")[0]

print(link)