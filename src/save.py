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
#* @param(string) path: path to the file
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
#* @param(string) user: user's account name
#* @param(string) path: folder path where the html will be saved: "../html/"
def save_other(user, path):
    tabs = ["", "?tab=repositories", "?tab=projects", "?tab=packages", "?tab=stars"]
    for tab in tabs:
        home = "https://github.com/" +  user
        url = home + tab
        file_name = path + fix_url(url)
        if test_path(file_name):
            return
        html = requests.get(url)
        if not html:
            print("invalid github link", url)
            return
        html_to_file(file_name, html.text)

#* @brief: all followers and following of a user, depending on the tab
#* @param(string) user: user's account name
#* @param(string) path: folder path where the html will be saved: "../html/"
#* @param(string) tab: the user type to save ["followers", "following"]
def save_users(user, path, tab):
    page = 1
    while 1:
        home = "https://github.com/" +  user
        url = home + "?page=" + str(page) + "&tab=" + tab
        file_name = path + fix_url(url)
        if not test_path(file_name):
            html = requests.get(url)
            if not html:
                print("invalid github link", url)
                return
            bfsO = BeautifulSoup(html.text, "html.parser")
            users = bfsO.findAll("a", {"data-hovercard-type": "user"})
            span = bfsO.findAll("span", {"class": "user-following-container"})
            #! jankey wa to tell that you've reached the last page of users
            if len(span) <= 1:
                return
            if users:
                html_to_file(file_name, html.text)
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

if __name__ == "__main__":
    user = sys.argv[1] # "conorosully"
    path = sys.argv[2] #"../html/"
    save_all(user, path)
    print("works")