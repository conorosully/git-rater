import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#?#################################################
# TODO
#?#################################################
# I want to make this a general function for all the tabs


#?#################################################
#? file functions
#?#################################################

def fix_path(path):
    return "../html/" + path.replace("/","%fs%")

def test_path(path):
    try:
        open(path, "r")
    except IOError:
        return 0
    return 1  

#! will the last newline be a problem?
def friends_to_file(path, friends):
    fp = open(path, "w")
    for friend in friends:
        fp.write(friend + "\n")
    fp.close()

def html_to_file(path, html):
    path = fix_path(path)
    fp = open(path, "w")
    fp.write(html)
    fp.close()

def file_to_html(path):
    path = fix_path(path)
    html = ""
    if not test_path:
        return None
    for line in open(path, "r"):
        html+=line
    return html

#?#################################################
#? scrape functions
#?#################################################

def save_friends(home, tab):
    friends = {}
    page = 1
    while 1:
        flag = 1
        url = home + "?page=" + str(page) + "&tab=" + tab
        if test_path(fix_path(url)):
            flag = 0
        if flag:
            html = requests.get(url)
            if not html:
                print("invalid github link", home)
                return
            bfsO = BeautifulSoup(html.text, "html.parser")
            users = bfsO.findAll("a", {"data-hovercard-type": "user"})
            if users:
                html_to_file(url, html.text)
            else:
                return
        page += 1

def get_friends(home, tab):
    friends = {}
    page = 1
    while 1:
        url = home + "?page=" + str(page) + "&tab=" + tab
        if not test_path(fix_path(url)):
            return friends
        html = file_to_html(url)
        bfsO = BeautifulSoup(html, "html.parser")
        users = bfsO.findAll("a", {"data-hovercard-type": "user"})
        if not users:
            return friends
        for user in users:
            href = user.get("href")
            href = href[1:len(href)]
            friends[href] = href
        for friend in friends:
            (friend)
        page += 1
    return friends


#?#################################################
#? main
#?#################################################

def main():
    # url = "https://github.com/m4d4rchy"
    # url = "https://github.com/conorosully"
    # url = "https://github.com/fabpot"
    if len(sys.argv) < 3:
        print("Invalid input\n<python3 friends.py> <user_name> <file>")
        return

    url = "https://github.com/" +  sys.argv[1]
    tab = "followers"
    save_friends(url, tab)
    friends = get_friends(url, tab)
    path = sys.argv[2]
    print(friends)
    if not test_path(path):
        friends_to_file(path, friends)

if __name__ == "__main__":
    main()
