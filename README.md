# github-rater
A machine learning model that tries to predict the quality of your github profile <br>
<b>Medium article: </b> coming soon <br>
<b>Dataset: </b>https://www.kaggle.com/conorsully1/github-ratings 
<table>
  <tr>
    <th>File</th>
    <th><span style="font-weight:bold">Description</span></th>
  </tr>
  <tr>
    <td>save.py</td>
    <td>Collection of functions used to scrape and save GitHub profile html</td>
  </tr>
  <tr>
    <td>capture.py</td>
    <td>Collection of functions used to extract specific elements from html (i.e. list of contributions)</td>
  </tr>
  <tr>
    <td>collect_data.ipynb</td>
    <td>Notebook used to collect GitHub profile data for a given list of users</td>
  </tr>
  <tr>
    <td>feature_engineering.ipynb</td>
    <td>Create model features from saved profile data</td>
  </tr>
  <tr>
    <td>decision_tree.ipynb</td>
    <td>Build a decison tree to predict the ratings of github profiles</td>
  </tr>
  <tr>
    <td>random_forest.ipynb</td>
    <td>Build a random forest to predict the ratings of github profiles</td>algorithm.</td>
  </tr>
</table>


## How to
### Web scrapper 
<b>Note: </b> this code is outdate and will need to be updated to run on the new GitHub layout
<br>
First download the html of a users profile: 
```python
import save as sv #save html
import capture as cp #obtain features

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
