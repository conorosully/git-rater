import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import datetime

#?#################################################
#? helper functions
#?#################################################

#* @brief: turns strings into ints that are scaled by strings ie "11.2k" --> 11200
#* @param(string) string: string rep of an int
#* @return(int): return the int
def str_to_int(string):
    if string.find("k") > 0:
        string = string.replace("k", "")
        return int(float(string)*1000)
    return int(string)

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
        open(path, "r")
    except IOError:
        return 0
    return 1

#* @brief: gets html as string from a saved file
#* @param(string) path: the path of the file that has been saved
#* @return(string): the html string if, if it exists else None
def file_to_html(path):
    html = ""
    if not test_path:
        return None
    for line in open(path, "r"):
        html+=line
    return html


#?#################################################
#? scrape functions
#?#################################################

#* @brief: returns an dic of the tab counts visible from overvief page
#* @param(string) user: user's account name
#* @param(string) path: folder path where the html will be saved: "../html/"
#* @return counts: returns dic - #repos #projects #stars #followers #following
def get_counts(user, path):
    struct = {}
    home = "https://github.com/" +  user
    file_name = path + fix_url(home)
    if not test_path(file_name):
        return None
    html = file_to_html(file_name)
    bfsO = BeautifulSoup(html, "html.parser")
    counts = bfsO.findAll("span", {"class": "Counter"})
    struct["repos"] = str_to_int(counts[0].text.strip())
    struct["projects"] = str_to_int(counts[1].text.strip())
    struct["stars"] = str_to_int(counts[2].text.strip())
    struct["followers"] = str_to_int(counts[3].text.strip())
    struct["following"] = str_to_int(counts[4].text.strip())
    return struct

#* @brief: returns an array of all the users a user follows/following
#* @param(string) user: user's account name
#* @param(string) path: folder path where the html will be saved: "../html/"
#* @param tab: which type of user to parse ["following", "followers"]
#* @return friends: array of all friends
def get_friends(user, path, tab):
    home = "https://github.com/" +  user
    friend_hash = {}
    friends = []
    page = 1
    while 1:
        url = home + "?page=" + str(page) + "&tab=" + tab
        file_name = path + fix_url(url)
        if not test_path(file_name):
            return friends
        html = file_to_html(file_name)
        bfsO = BeautifulSoup(html, "html.parser")
        users = bfsO.findAll("a", {"data-hovercard-type": "user"})
        if not users:
            return friends
        for user in users:
            href = user.get("href")
            href = href[1:len(href)]
            if not friend_hash.get(href, 0):
                friend_hash[href] = href
                friends.append(href)
        page += 1
    return friends

#* @brief: get repo information from repositiories tab
#* @param(string) user: user's account name
#* @param(string) path: folder path where the html will be saved: "../html/"
#* @return(dic): returns an dic nesting 3 arrays
    #* @return(dic[0]) returns list of titles of the repos
    #* @return(dic[1]) returns a list of lanauges of the repos (not in parallel with titles)
    #* @return(dic[2]) returns a list of when the repo was last modified (in parallel with titles)
def get_repos(user, path):
    home = "https://github.com/" +  user
    struct = {}
    titles = []
    langs = []
    dates = []
    url = home + "?tab=" + "repositories"
    file_name = path + fix_url(url)
    if not test_path(file_name):
        return struct
    html = file_to_html(file_name)
    bfsO = BeautifulSoup(html, "html.parser")
    user_list = bfsO.find("div", {"id": "user-repositories-list"})
    a = user_list.findAll("a")
    span = user_list.findAll("span", {"itemprop": "programmingLanguage"})
    relt = user_list.findAll("relative-time")
    for x in a:
        titles.append(x.get("href").replace("/" + user + "/", ""))
    for x in span:
        langs.append(x.text)
    for x in relt:
        dates.append(x.text)
    struct["name"] = titles
    struct["languages"] = langs
    struct["last_commit"] = dates
    return struct

#* @brief: get contribution information from overview
#* @param(string) user: user's account name
#* @param(string) path: folder path where the html will be saved: "../html/"
#* @return(array of arrays): returns [[commits, day]]
def get_contributions(user, path):
    home = "https://github.com/" +  user
    data = []
    url = home
    file_name = path + fix_url(home)
    if not test_path(file_name):
        return
    html = file_to_html(file_name)
    bfsO = BeautifulSoup(html, "html.parser")
    con = bfsO.find("div", {"class": "js-yearly-contributions"})
    rect = con.findAll("rect")
    for r in rect:
        d = []
        d.append(r.get("data-date"))
        d.append(r.get("data-count"))
        data.append(d)
    return data

# def main():
#     user = "conorosully"
#     path = "../html/"
#     counts = get_counts(user, path)
#     print(counts)
#     followers = get_friends(user, path, "followers")
#     print(followers)
#     following = get_friends(user, path, "following")
#     print(following)
#     repos = get_repos(user, path)
#     print(repos)
#     con = get_contributions(user, path)
#     print(con)
#     print("works")

# main()