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

# def save_overview(home, tab):
#     friends = {}
#     page = 1
#     while 1:
#         flag = 1
#         url = home
#         if test_path(fix_path(url)):
#             flag = 0
#         if flag:
#             html = requests.get(url)
#             if not html:
#                 print("invalid github link", home)
#                 return
#             bfsO = BeautifulSoup(html.text, "html.parser")
#             users = bfsO.findAll("a", {"data-hovercard-type": "user"})
#             if users:
#                 html_to_file(url, html.text)
#             else:
#                 return
#         page += 1

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


#?#################################################
#? main
#?#################################################

def main():
    # url = "https://github.com/m4d4rchy"
    # url = "https://github.com/conorosully"
    # url = "https://github.com/fabpot"
    if len(sys.argv) < 1:
        print("Invalid input\n<python3 untitled_scraper.py> <user_name>")
        return
    url = "https://github.com/" + sys.argv[1]
    counts = get_metrics(url)
    print(counts)

if __name__ == "__main__":
    main()
