import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#?#################################################
#? file functions
#?#################################################
#* @brief: removes backlashes from a url so that it can be used as a file name
#* @param(string) url: url of the html that will be saved
#* @return(string): the url with backslashes substituted
def fix_path(url):
    return sys.argv[2] + url.replace("/","%fs%")

#* @brief: tests if a file exists
#* @param(string) url: url of the html that will be saved
#* @return(int): 1 if file exists else 0
def test_path(url):
    try:
        fp = open(url, "r")
        fp.close()
    except IOError:
        return 0
    return 1  

#* @brief: saves string html to a file
#* @param(string) path: the path of the file that will be saved
#* @param(string) html: string version of a page's html
def html_to_file(path, html):
    fp = open(path, "w")
    fp.write(html)
    fp.close()

#?#################################################
#? save functions
#?#################################################

#* @brief: saves overview, repos, project and stars of a user (just the 1st page of each)
#* @param(string) home: url to a user's overview page. "https://github.com/user_name"
def save_other(home):
    tabs = ["", "?tab=repositories", "?tab=projects", "?tab=packages", "?tab=stars"]
    for tab in tabs:
        url = home + tab
        if test_path(fix_path(url)):
            return
        html = requests.get(url)
        if not html:
            print("invalid github link", home)
            return
        html_to_file(fix_path(url), html.text)

#* @brief: all followers and following of a user, depending on the tab
#* @param(string) home: url to a user's overview page
#* @param(string) tab: the user type to save ["followers", "following"]
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

#* @brief: function that calls all the save functions
def save_all():
    if len(sys.argv) < 3:
        print("Invalid input\n<python3 save.py> <user_name> <path_to_save_folder>")
        return
    home = "https://github.com/" +  sys.argv[1]
    save_users(home, "followers")
    save_users(home, "following")
    save_other(home)
