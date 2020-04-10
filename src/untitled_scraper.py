import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import datetime

#?#################################################
#? helper functions
#?#################################################

def str_to_int(string):
    if string.find("k") > 0:
        string = string.replace("k", "")
        return int(float(string)*1000)
    return int(string)


#?#################################################
#? scrape functions
#?#################################################

# @param url: string leading to a user's overview page; "https://github.com/user_name"
# @return counts: returns an array - #repos #projects #stars #followers #following
def get_metrics(url):
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

def get_friends(home):
    friends = {}
    page = 1
    while 1:
        url = home + "?page=" + str(page) + "&tab=followers"
        html = requests.get(url)
        if not html:
            print("invalid github link")
            return 
        bfsO = BeautifulSoup(html.text, "html.parser")
        users = bfsO.findAll("a", {"data-hovercard-type": "user"})
        if not users:
            return friends
        for user in users:
            href = user.get("href")
            href = href[1:len(href)]
            friends[href] = href

        # for friend in friends:
        #     print(friend)
        page += 1


#?#################################################
#? main
#?#################################################

def main():
    url = "https://github.com/m4d4rchy"
    # url = "https://github.com/conorosully"
    # url = "https://github.com/fabpot"
    
    counts = get_metrics(url)
    print(counts)
    # # friends = get_friends(url)
    # # for friend in friends:
    #     print(friend)

if __name__ == "__main__":
    main()
