       ## Import required modules
import requests # for GET request from API
import os # for saving access tokens
import pandas as pd # for displaying data
import json # for handelling JSON data/ file
import base64 # to generate single encoded key for twitter
import pyodbc # to connect python to sql
import numpy as np # for list manipulation
from time import sleep # to delay get requests (so you don't get banned by twitter!)





#######################################################################################################################
    ## Create access token
#######################################################################################################################
# Code derived from: https://benalexkeen.com/interacting-with-the-twitter-api-using-python/

# Set up Twitter app and get Client (API) Key and Client (API) Secret
client_key = 'apiKey' # add your API Key
client_secret = 'apiKeySecret' # add your API Key Secret

# Twitter API requires single key that is a string of a base64 encoded version of the two keys seperated by a colon
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

# Request authentication endpoint
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

# Check status code okay
auth_resp.status_code

# Keys in data response are token_type (bearer) and access_token (your access token)
auth_resp.json().keys()

# Create access token
access_token = auth_resp.json()['access_token']





#######################################################################################################################
    ## Make a GET request
#######################################################################################################################
# Code derived from https://benalexkeen.com/interacting-with-the-twitter-api-using-python/

# Access token required for making GET request
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}

# Define parameters for GET request
# Parameters explained here https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets, and here https://developer.twitter.com/en/docs/twitter-api/fields
search_params = {
    'q': 'dogs', # search for content containing this string
    'result_type': 'mixed', # can be set to return most 'recent', 'popular', or 'mixed' result
# Tweets made between specified start and end date
    #'start_time': '2015--07-19', # tweets made after this date
    #'until': '2019-08-19', # tweets created before this date. Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.
    'expansions': 'author_id', # get author (user) information
    'user.fields': 'description', # return users profile description
    'count': 100, # number of results returned (defult 15, up to 100 tweets can be requested), be warned, twitter will give tweets up to the number specified, so it may not return exactly 100 if you say 100
# Filter out retweets or replies from results (if you filter out both, you will not recieve any results, unless you have twitter premium)
    #'exclude': 'retweets' # filter out retweets from results
    'exclude': 'replies' # filter out replies from results
}

search_url = '{}1.1/search/tweets.json'.format(base_url)

# Make GET request multiple times and store output in list
tweet_data = []
i = 0
while i < 4: # define the maximum number of GET requests you want to make. Note that twitter may return duplicate tweets when making multiple GET requests.
    search_resp = requests.get(search_url, headers=search_headers, params=search_params).json()
    tweet_data.append(search_resp)
    i = i + 1
    sleep(5) # delay GET request (seconds) so Twitter doesn't mistake you for spam (if you make multiple API requests too quickly then Twitter will block your app)





#######################################################################################################################
    ## Save output as JSON
#######################################################################################################################

# Save the GET request output as a JSON file
#with open('filePath/fileName.json', 'w') as outfile:
#    json.dump(tweet_data, outfile)

# Open JSON file containing tweet data
#with open('filePath/fileName.json') as f:
#  tweet_data = json.load(f)





#######################################################################################################################
    ## Format output data
#######################################################################################################################

# Extract information of interest
my_list = [] # store tweet information in a list
for index in range(len(tweet_data)): # multiple GET requests produces multiple arrays in output that you need to loop through
    for status in tweet_data[index]['statuses']: # loop through multiple tweets for each GET request output
      my_list.append(status['created_at']) # date tweet was made
      my_list.append(status['user']['name']) # users name
      my_list.append(status['user']['location']) # user location
      my_list.append(status['lang']) # language
      my_list.append(status['user']['followers_count']) # how many followers user has
      my_list.append(status['user']['friends_count']) # how many friends user has
      my_list.append(status['favorite_count']) # number of like for particular tweet
      my_list.append(status['retweeted']) # if tweet was retweeted 

# Split list of tweet info based on number of tweets
# this produces a matrix of multiple lists, with each list containing data for a single tweet
splitBy = (len(my_list)/8) # number of tweets calculated by dividing length of list by number of list appended values (values such as created_at, user name, user location, etc)
tweet_matrix = np.matrix(np.array_split(my_list, splitBy)) # split list by number of tweets to produce lists for each tweet, and convert this to a matrix

# Convert tweet matrix into a dataframe
tweet_df = pd.DataFrame(tweet_matrix, columns = ['date_posted' , 'user_name', 'location', 'language', 'followers', 'friends', 'post_likes', 'retweeted']) # column names





#######################################################################################################################
    ## Send data to SQL
#######################################################################################################################
# Code derived from: https://datatofish.com/how-to-connect-python-to-sql-server-using-pyodbc/

# Find out what drivers are available to you
print(pyodbc.drivers())

# Connect to SQL
conn = pyodbc.connect('Driver={SQL Server};' # use SQL server if you are connecting to SQL with username and password
                      'Server=serverName.database.windows.net;' # server name
                      'Database=databaseName;' # database name
                      #'Trusted_Connection=yes;' # only unhash this if you have windowns authenification, and if you do unhash this then hash out user name and password
                      'Schema=schemaName;' # schema
                      'UID=userName;' # username
                      'PWD=password;' # password
                      )

cursor = conn.cursor() # open connection


# Create table in SQL 
# Code from https://datatofish.com/import-csv-sql-server-python/
cursor.execute('''
		CREATE TABLE tweets (
			date_posted nvarchar(max),
			user_name nvarchar(max),
                        location nvarchar(max),
                        language nvarchar(max),
                        followers int,
                        friends int,
                        post_likes int,
                        retweeted nvarchar(max)
			)
               ''')



# Insert data from dataframe into SQL table
for row in tweet_df.itertuples(): # for every row in you df
    cursor.execute('''
                INSERT INTO tweets (date_posted, user_name, location, language, followers, friends, post_likes, retweeted)
                VALUES (?,?,?,?,?,?,?,?)
                ''',
                row.date_posted,
                row.user_name,
                row.location,
                row.language,
                row.followers,
                row.friends,
                row.post_likes,
                row.retweeted
                )
conn.commit()

# Always close connection when you are finished with SQL
conn.close()  

# Now go to Microsoft SQL Server Management Studio (SSMS) and connect to Azure SQL database. Here, you can query database.
