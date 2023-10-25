from flask import Flask, render_template, url_for

from scraper import scrape
from time import sleep
import requests
import json
from urllib.request import urlretrieve
from flask import Flask, request
from flask_cors import CORS
from bson import json_util
import os
import pandas as pd
from flatten_json import flatten
import re


def get_videodata(link, key):
    link = link["url"]
    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
    querystring = {"url":link,"hd":"1"}
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    video_data = requests.get(url, headers=headers, params=querystring)
    video_data = video_data.json()["data"]

    return video_data


def get_comments(link, key):
    link = link["url"]
    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/comment/list"
    querystring = {"url":link,"count":"50","cursor":"0"}
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    comment_data = requests.get(url, headers=headers, params=querystring)
    comment_data = comment_data.json()["data"]["comments"]

    return comment_data


def download_video(link):
    file_name = "video.mp4"
    urlretrieve(link, file_name)

def download_video_local(link, username, id):
    file_name = f'./brukere/videos/{username}/{id}.mp4'
    urlretrieve(link, file_name)



app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('base.html')

def parse_json(data):
    return json.loads(json_util.dumps(data))


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


@app.route('/scrape_serve',methods=['POST'])
def scrape_serve():

    try:

        #log the body of the request
        print(request.json)
        brukere = request.json["brukernavn"]
        api_key = request.json["key"]

        #split at the commas
        brukere = brukere.split(",")
        #if there are semicolons, split at the semicolons instead
        brukere = [bruker.split(";") for bruker in brukere]
        #flatten the list
        brukere = [item for sublist in brukere for item in sublist]
        #remove any whitespace
        brukere = [bruker.strip() for bruker in brukere]

        #remove newlines
        brukere = [bruker.replace("\n", "") for bruker in brukere]

        print(brukere)


        for bruker in brukere:
            newpath = f'./brukere/' + bruker + '/videos'
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            newpath = f'./brukere/' + bruker + '/data'
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            scrape(bruker)

            with open(f'./brukere/{bruker}/data/links.json') as f:
                data = json.load(f)

            links = data[0]["videoer"]
            print(links)

            videos = []
            comments = []

            ny_bruker = [
                {
                    "username": bruker,
                    "displayname": data[0]["displayname"],
                    "following_count": data[0]["following_count"],
                    "followers_count": data[0]["followers_count"],
                    "likes_count": data[0]["likes_count"],
                    "desc": data[0]["desc"],
                    "videos": []
                }
            ]

            for link in links:
                ny_video = {
                    "link": link,
                    "video_data": get_videodata(link, api_key),
                    "comment_data": get_comments(link, api_key),
                }


                ny_bruker[0]["videos"].append(ny_video)

                try:
                    urlretrieve(ny_video["video_data"]["play"], f"./brukere/{bruker}/videos/{ny_video['video_data']['id']}.mp4")
                    print("Video nedlastet")
                    print("video id er: " + ny_video["video_data"]["id"])
                except Exception as e:
                    print(e)
                    print("Noe gikk galt, fortsetter med neste video")
                    continue

                video_data = ny_video["video_data"]
                comment_data = ny_video["comment_data"]
                videos.append(video_data)
                comments.append(comment_data)

            #flatten the json
            videos = [flatten_json(video) for video in videos]
            comments = [flatten_json(comment) for comment in comments]

            ny_comments = []

            for comment in comments:
                video = videos[comments.index(comment)]
                video_id = video["id"]

                i = 0
                for key in comment:
                    # nøkkelen print(key)
                    # verdien print(comment[key])


                    if i % 24 == 0:
                        ny_comments.append({})
                        ny_comments[-1]["video_id"] = video_id

                    new_key = re.sub(r'\d+', '', key)
                    new_key = new_key[1:]

                    if new_key == "id":
                        new_key = "comment_id"

                    ny_comments[-1][new_key] = comment[key]
                    i += 1

            print(ny_comments)

            comments = ny_comments


            #convert to dataframe
            videos = pd.DataFrame(videos)
            comments = pd.DataFrame(comments)


            #save to csv
            videos.to_csv(f'./brukere/{bruker}/data/videos.csv')
            comments.to_csv(f'./brukere/{bruker}/data/comments.csv')

        return "Ferdig"
    except Exception as e:
        print(e)
        return "Noe gikk galt", 404



if __name__ == '__main__':
    app.run(debug=True)


#semikolon må funke
#omformater json til csv
