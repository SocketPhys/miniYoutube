from __future__ import print_function # In python 2.7
from flask import Flask,render_template, request
import yaml
import json
import requests
app = Flask(__name__)
API_KEY = yaml.load(open("settings.yml",'r').read())['API_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
@app.route("/")
def root():
     return render_template('start.html')
    
@app.route("/channel",methods=['POST'])
def load():     
     CHANNEL= request.form['channel']
     TAG = request.form['tag']
     if not CHANNEL:
        try:
            url = searchByTag(TAG)
            return render_template('load.html',url=url)
        except:
            return render_template('errorTag.html')
     
     try:
        url = searchByUserLink(CHANNEL)
        return render_template('load.html',url=url)
     except:
        try:
            url = searchByUserLink(CHANNEL)
            return render_template('load.html',url=url)
        except:
            try:
                url = searchByUsername(CHANNEL)
                return render_template('load.html',url=url)
            except:
                return render_template('error.html')

def searchByTag(tag):
     TAG = tag
     response = requests.get("https://www.googleapis.com/youtube/v3/search?key=" + API_KEY + "&q=" + TAG + "&part=id&order=date&maxResults=20")
     response = json.loads(response.text)
     url=[]
     for i in range(0,len(response['items'])):
        result = response.get('items', {})[i].get('id', {}).get('videoId')
        if result:
            url.append("http://www.youtube.com/v/" + result)
     
     return url 

def searchByUserLink(user):
    USER=user

    ID  = USER[USER.index('https://www.youtube.com/user/')+29:]
    return searchByChannelId(ID)
   
  
 
def searchByUsername(username):
    USERNAME=username
    USERNAME =requests.get("https://www.googleapis.com/youtube/v3/channels?key=" + API_KEY + "&forUsername=" + USERNAME + "&part=id")
    USERNAME =json.loads(USERNAME.text)
    ID= USERNAME['items'][0]['id']
    return searchByChannelId(ID)
   
def searchByChannelLink(channel):
    CHANNEL = channel
    ID =  CHANNEL[CHANNEL.index('https://www.youtube.com/channel/')+32:]
    return searchByChannelId(ID)
 
    

def searchByChannelId(ID):
    response = requests.get("https://www.googleapis.com/youtube/v3/search?key=" + API_KEY + "&channelId=" + ID  + "&part=id&order=date&maxResults=20")
    response = json.loads(response.text)
    url=[]
    for i in range(0,len(response['items'])):
       result = response.get('items', {})[i].get('id', {}).get('videoId')
       if result:
           url.append("https://www.youtube.com/v/" + result)
    return url


    


