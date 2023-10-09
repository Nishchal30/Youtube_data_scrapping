import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


logging.basicConfig(filename="youtube_scarpping_logs.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

def get_channel_ID(youtube, channel_name):
    '''
    This fuction is used to provide the channel ID of the channel by passing the youtuber name using youtube api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param youtube_name: type: <String>, It is the name of youtuber
    :return: type: <string>, The string contains the username of youtuber channel fetched using youtube api
    '''

    try:
        search_response = youtube.search().list(
        q=channel_name,
        type="channel",
        part="id"
        ).execute()
    
        channel_ID = search_response['items'][0]['id']['channelId']
        return channel_ID

    except Exception as e:
        logging.info(f"something went wrong {e}")


    if __name__=='__main__':
        from googleapiclient.discovery import build
        DEVELOPER_KEY = "AIzaSyAaeo-q3kZLtB8G6QKCvQoz6eB3J-oN2Cw"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)   
        print(get_channel_ID(youtube,"krish naik"))