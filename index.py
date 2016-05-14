from __future__ import print_function # In python 2.7
from flask import Flask,render_template, request
import yaml
import json
import requests
application = Flask(__name__)
API_KEY = yaml.load(open("settings.yml",'r').read())['API_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
@application.route("/")
def root():
     return render_template('start.html')
    
@application.route("/channel",methods=['POST'])
def load():
     CHANNEL= request.form['channel']
     try:
        CHANNEL = CHANNEL[CHANNEL.index('https://www.youtube.com/user/')+29:]
        CHANNEL =requests.get("https://www.googleapis.com/youtube/v3/channels?key=" + API_KEY + "&forUsername=" + CHANNEL + "&part=id")
        CHANNEL =json.loads(CHANNEL.text)
        CHANNEL = CHANNEL['items'][0]['id']
     except:
        try:
            CHANNEL = CHANNEL[CHANNEL.index('https://www.youtube.com/channel/')+32:]
        except:
            try:
                 CHANNEL =requests.get("https://www.googleapis.com/youtube/v3/channels?key=" + API_KEY + "&forUsername=" + CHANNEL + "&part=id")
                 CHANNEL =json.loads(CHANNEL.text)
                 CHANNEL = CHANNEL['items'][0]['id']
            except:
                 return render_template('error.html')        
     response = requests.get("https://www.googleapis.com/youtube/v3/search?key=" + API_KEY + "&channelId=" + CHANNEL + "&part=id&order=date&maxResults=20")
     response = json.loads(response.text)
     url=[]
     for i in range(0,len(response['items'])):
        result = response.get('items', {})[i].get('id', {}).get('videoId')
        if result:
            url.append("http://www.youtube.com/v/" + result)


     return render_template('load.html',url=url)
 
if __name__ == "__main__":
    
   application.debug = True
   application.run(host='127.0.0.1')
