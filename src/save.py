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

#! these methods wo=ill be moved to capture.py
def get_friends(home, tab):
    friends = {}
    page = 1
    while 1:
        url = home + "?page=" + str(page) + "&tab=" + tab
        if not test_path(fix_path(url)):
            return friends
        html = file_to_html(fix_path(url))
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

def get_repos(home, tab):
    repos = []
    titles = []
    langs = []
    url = home + "?tab=" + tab
    if not test_path(fix_path(url)):
        return repos
    html = file_to_html(fix_path(url))
    bfsO = BeautifulSoup(html, "html.parser")
    user_list = bfsO.find("div", {"id": "user-repositories-list"})
    a = user_list.findAll("a")
    span = user_list.findAll("span", {"itemprop": "programmingLanguage"})
    relt = user_list.findAll("relative-time")
    # print(user_list)
    # print(a)
    for x in a:
        titles.append(x.get("href"))
    for x in span:
        langs.append(x.text)
    for x in relt:
        print(x.text)

def get_overview(home):
    url = home
    if not test_path(fix_path(url)):
        return
    html = file_to_html(fix_path(url))
    bfsO = BeautifulSoup(html, "html.parser")
    con = bfsO.find("div", {"class": "js-yearly-contributions"})
    h2 = con.find("h2")
    rect = con.findAll("rect")
    print(h2.text.strip())
    data = []
    for r in rect:
        d = []
        d.append(r.get("data-date"))
        d.append(r.get("data-count"))
        data.append(d)
    print(data)
    print("end overview")


#! bsbsbsb print


#?#################################################
#? main
#?#################################################

def main():
    # home = "https://github.com/m4d4rchy"
    # home = "https://github.com/conorosully"
    # home = "https://github.com/fabpot"
    if len(sys.argv) < 3:
        print("Invalid input\n<python3 friends.py> <user_name> <file>")
        return

    save_all()

    #! bs print    
    home = "https://github.com/" +  sys.argv[1]
    friends = get_friends(home, "followers")
    print("followers", friends)
    friends = get_friends(home, "following")
    print("following", friends)
    repos = get_repos(home, "repositories")
    print("repos", repos)
    get_overview(home)



    path = sys.argv[2]
    if not test_path(path): #! this will be moved to capture.py
        friends_to_file(path, friends)

if __name__ == "__main__":
    main()
