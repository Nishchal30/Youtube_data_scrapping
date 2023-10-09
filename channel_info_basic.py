# import logging
import googleapiclient.errors

# logging.basicConfig(filename="youtube_scarpping_logs.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

def get_channel_info(youtube, channel_ID):

    '''
    This fuction is used to provide the channel info of the channel by passing the channel ID of channel using youtube api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param youtube_name: type: <String>, It is the username of the channel
    :return: type: <dictionary>, The dictionary contains the information of that youtube channel like channel_ID, Playlist_ID, channel_name fetched using youtube api
    '''

    try:
        channel_info = {}
        channel_response = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id = channel_ID
        ).execute()
        
        channel_info = dict(
        channel_id = channel_response.get("items", [])[0]['id'],
        channel_name = channel_response.get("items", [])[0]['snippet']['title'],
        playlist_ID = channel_response.get("items", [])[0]['contentDetails']['relatedPlaylists']['uploads']
        # subscriber_count = channel_response.get("items", [])[0]['statistics']['subscriberCount'],
        # video_count = channel_response.get("items", [])[0]['statistics']['videoCount']
        )

        return channel_info
    
    except googleapiclient.errors.HttpError as e:
        status_code = e.resp.status
        error_message = e.content.decode("utf-8")
        print(f"HTTP status code: {status_code}")
        print(f"Error message: {error_message}")


    if __name__=='__main__':
        from googleapiclient.discovery import build
        DEVELOPER_KEY = YOUR_API_KEY
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)   
        # print(youtube)
        # print(get_channel_info(youtube,"krish naik"))