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
    fp = open(path, "w")
    fp.write(html)
    fp.close()

def file_to_html(path):
    html = ""
    if not test_path:
        return None
    for line in open(path, "r"):
        html+=line
    return html

#?#################################################
#? save functions
#?#################################################

def save_overview(home):
    url = home
    if test_path(fix_path(url)):
        return
    html = requests.get(url)
    if not html:
        print("invalid github link", home)
        return
    html_to_file(fix_path(url), html.text)

def save_other(home, tab):
    url = home + "?tab=" + tab
    if test_path(fix_path(url)):
        return
    html = requests.get(url)
    if not html:
        print("invalid github link", home)
        return
    html_to_file(fix_path(url), html.text)

def save_users(home, tab):
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
                html_to_file(fix_path(url), html.text)
            else:
                return
        page += 1

def save_all():
    url = "https://github.com/" +  sys.argv[1]
    save_users(url, "followers")
    save_users(url, "following")
    save_other(url, "repositories")
    save_other(url, "projects")
    save_other(url, "packages")
    save_other(url, "stars")
    save_overview(url)

#?#################################################
#? main
#?#################################################

def main():
    # home = "https://github.com/m4d4rchy"
    # home = "https://github.com/conorosully"
    # home = "https://github.com/fabpot"
    if len(sys.argv) < 2:
        print("Invalid input\n<python3 friends.py> <user_name>")
        return

    save_all()

if __name__ == "__main__":
    main()
