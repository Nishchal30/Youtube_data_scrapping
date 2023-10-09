from flask import Flask, render_template, request,redirect,send_file
from googleapiclient.discovery import build
from channel_ID import get_channel_ID
from channel_info_basic import get_channel_info
from Scrap_All_Videos import get_all_video_ID
from channel_info_medium import get_video_details
from remove_shorts_videos import remove_shorts_videos
from final_video_info import get_final_video_details
import pymongo
import logging

logging.basicConfig(filename="youtube_scarpping_logs.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

try:

    DEVELOPER_KEY = "AIzaSyAaeo-q3kZLtB8G6QKCvQoz6eB3J-oN2Cw"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)   

    client = pymongo.MongoClient("mongodb+srv://Nishchal30:Nishchal30@cluster0.9omin78.mongodb.net/")
    db = client['youtube_data']
    channel_data = db['channel_info']
    video_data = db['video_data']

    logging.info("The connection for the Mongo DB is successfully established and the data bases are created successfully")

except Exception as e:
    print(e)


app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():

    logging.info("The index page will load here")
    return render_template("index.html")


@app.route("/info", methods = ['GET', 'POST'])
def get_username():

    try:
        youtuber_name = request.form['search_for']
        logging.info(f"The data for the youtube channel {youtuber_name} will start here")

        channel_ID = get_channel_ID(youtube, youtuber_name)
        logging.info(f"The username for the {youtuber_name} is {channel_ID}")

        channel_data_exists = db['channel_info'].find_one({'channel_id': channel_ID})
            
        if channel_data_exists:
            video_data_exists = db['video_data'].find({'channel_ID': channel_ID})
            video_data_list = list(video_data_exists)  

            if video_data_list:
                for video in video_data_list:
                    video['_id'] = str(video['_id'])
                
            # return video_data_list

            return render_template("results.html", reviews=video_data_list)
        
        else:
            channel_info = get_channel_info(youtube, channel_ID)
            logging.info(f"The channel basic info is collected successfully")

            channel_video_dict = get_all_video_ID(youtube, channel_info['playlist_ID'])
            logging.info(f"The video IDs for the channel is collected successfully")

            video_info = get_video_details(youtube, channel_video_dict)
            logging.info(f"The video information for the video IDs is captured")

            final_video_ids = remove_shorts_videos(youtube, video_info, channel_video_dict, channel_info)
            logging.info(f"The final video IDs after removing shorts video IDs are collected here")

            final_video_info = get_final_video_details(youtube, final_video_ids)
            logging.info(f"The final video IDs information is collected successfully")

            channel_data.insert_one(channel_info)
            logging.info(f"The data for channel is stored in the Mongo DB")

            for i in final_video_info:
                video_data.insert_one(i)
            
            logging.info(f"The video data for the channel {youtuber_name} is stored in the Mongo DB")

            # return final_video_info
            return render_template("results.html", reviews=final_video_info)

    except Exception as e:
        print(f"Something went wrong {e}")


if __name__ == "__main__":
    app.run(debug=True)