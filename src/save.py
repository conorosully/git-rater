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
def fix_url(url):
    return url.replace("/","%fs%")

#* @brief: tests if a file exists
#* @param(string) url: url of the html that will be saved
#* @return(int): 1 if file exists else 0
def test_path(path):
    try:
        fp = open(path, "r")
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
def save_other(user, path):
    tabs = ["", "?tab=repositories", "?tab=projects", "?tab=packages", "?tab=stars"]
    for tab in tabs:
        home = "https://github.com/" +  user
        url = home + tab
        path += fix_url(url)
        if test_path(path):
            return
        html = requests.get(url)
        if not html:
            print("invalid github link", url)
            return
        html_to_file(path, html.text)

#* @brief: all followers and following of a user, depending on the tab
#* @param(string) home: url to a user's overview page
#* @param(string) tab: the user type to save ["followers", "following"]
def save_users(user, path, tab):
    page = 1
    while 1:
        home = "https://github.com/" +  user
        url = home + "?page=" + str(page) + "&tab=" + tab
        path += fix_url(url)
        if not test_path(path):
            html = requests.get(url)
            if not html:
                print("invalid github link", url)
                return
            bfsO = BeautifulSoup(html.text, "html.parser")
            users = bfsO.findAll("a", {"data-hovercard-type": "user"})
            if users:
                html_to_file(path, html.text)
            else:
                return
        page += 1

#* @brief: function that calls all the save functions
#* @param(string) user: a github user's name
#* @param(string) path: folder path to where you would like the html saved. eg: ../html/
def save_all(user, path):
    save_users(user, path, "followers")
    save_users(user, path, "following")
    save_other(user, path)
