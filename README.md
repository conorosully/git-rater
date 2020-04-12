# github-rater
A machine learning model that tries to predict the quality of your github profile

## How To
### Web Scrapper
First download the html of a users profile: 
```python
user = "conorosully"
path = "../data/test/"

#save html to folder
sv.save_all(user, path)
```

Then the features can be extracted: 
```python
#obtain features
counts = cp.get_counts(user, path)
followers = cp.get_friends(user, path, "followers")
following = cp.get_friends(user, path, "following")
repos = cp.get_repos(user, path)
cont = cp.get_contributions(user, path);
```
