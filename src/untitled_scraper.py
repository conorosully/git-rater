import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import datetime

def scrape_friends(url):
    search = "?tab=followers"
    html = requests.get(url + search)
    if not html:
        print("invalid github link")
        return
    bfsO = BeautifulSoup(html.text, "html.parser")
    users = bfsO.findAll("a", {"data-hovercard-type": "user"})
    
    friends = {}
    for user in users:
        href = user.get("href")
        href = href[1:len(href)]
        friends[href] = href

    for friend in friends:
        print(friend)

def str_to_int(string):
    if string.find("k") > 0:
        string = string.replace("k", "")
        return int(float(string)*1000)
    return int(string)

def get_repo_counts(url):
    html = requests.get(url)
    if not html:
        print("invalid github link")
        return
    bfsO = BeautifulSoup(html.text, "html.parser")
    counts = bfsO.findAll("span", {"class": "Counter"})
    result = []
    for i in range(len(counts)):
        counts[i] = counts[i].text.strip()
        counts[i] = str_to_int(counts[i])
    return counts

url = "https://github.com/conorosully"
# url = "https://github.com/fabpot"
# scrape_friends(url)
counts = get_repo_counts(url)
print(counts)