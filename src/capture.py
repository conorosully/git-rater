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

def print_struct(struct):
    counts = struct["counts"]
    followers = struct["followers"]
    following = struct["following"]
    repos = struct["repos"]
    con = struct["contributions"]
    
    print("{{counts: array[%d]}}"%(len(counts)))
    for i in range(len(counts)):
        if i == 0:
            print("repositories", counts[i])
        if i == 1:
            print("projects", counts[i])
        if i == 2:
            print("stars", counts[i])
        if i == 3:
            print("followers", counts[i])
        if i == 4:
            print("following", counts[i], "\n")
    print("{{followers: dictionary[%d] - indexed by follower's name}}"%(len(followers)))
    for f in followers:
        print(f)
    print("\n{{following: dictionary[%d] - indexed by follower's name}}"%(len(following)))
    for f in following:
        print(f)
    print("\n{{repos: array[%d]}}"%(len(repos)))
    print("{repos[0]: array[%d]} - project titles"%(len(repos[0])))
    for r in repos[0]:
        print(r)
    print("\n{repos[1]: array[%d]} - project languages"%(len(repos[1])))
    for r in repos[1]:
        print(r)
    print("\n{repos[2]: array[%d]} - last commit date"%(len(repos[2])))
    for r in repos[2]:
        print(r)
    print("\n{{con: array[%d]}} - [date, contribution]"%(len(con)))
    for c in con:
        print(c)


    



#?#################################################
#? file functions
#?#################################################
def fix_path(path):
    return sys.argv[2] + path.replace("/","%fs%")

def test_path(path):
    try:
        open(path, "r")
    except IOError:
        return 0
    return 1  

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

# @param url: string leading to a user's overview page; "https://github.com/user_name"
# @return counts: returns an array - #repos #projects #stars #followers #following
def get_counts():
    home = "https://github.com/" +  sys.argv[1]
    if not test_path(fix_path(home)):
        return None
    html = file_to_html(fix_path(home))
    bfsO = BeautifulSoup(html, "html.parser")
    counts = bfsO.findAll("span", {"class": "Counter"})
    for i in range(len(counts)):
        counts[i] = counts[i].text.strip()
        counts[i] = str_to_int(counts[i])
    return counts

def get_friends(tab):
    home = "https://github.com/" +  sys.argv[1]
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

def get_repos():
    home = "https://github.com/" +  sys.argv[1]
    repos = []
    titles = []
    langs = []
    dates = []
    url = home + "?tab=" + "repositories"
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
        dates.append(x.text)
    return [titles, langs, dates]

def get_contributions():
    home = "https://github.com/" +  sys.argv[1]
    data = []
    url = home
    if not test_path(fix_path(url)):
        return
    html = file_to_html(fix_path(url))
    bfsO = BeautifulSoup(html, "html.parser")
    con = bfsO.find("div", {"class": "js-yearly-contributions"})
    # h2 = con.find("h2")
    rect = con.findAll("rect")
    # print(h2.text.strip())
    for r in rect:
        d = []
        d.append(r.get("data-date"))
        d.append(r.get("data-count"))
        data.append(d)
    # print(data)
    # print("end overview")
    return data


# #?#################################################
# #? main
# #?#################################################

# def main():
#     # url = "https://github.com/m4d4rchy"
#     # url = "https://github.com/conorosully"
#     # url = "https://github.com/fabpot"
#     struct = {}
#     if len(sys.argv) < 1:
#         print("Invalid input\n<python3 untitled_scraper.py> <user_name>")
#         return
#     #! bs print    
#     home = "https://github.com/" +  sys.argv[1]
#     struct["counts"] = get_counts(home)
#     struct["followers"] = get_friends(home, "followers")
#     struct["following"] = get_friends(home, "following")
#     struct["repos"] = get_repos(home, "repositories")
#     struct["contributions"] = get_contributions(home)
#     print_struct(struct)

# if __name__ == "__main__":
#     main()
