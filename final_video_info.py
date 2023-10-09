# import logging
import googleapiclient.errors
from datetime import datetime as dt

# logging.basicConfig(filename="youtube_scarpping_logs.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

def get_final_video_details(youtube, video_list):

    '''
    This fuction is used to collect video information only for long videos using youtube api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param youtube_name: type: <String>, It is the username of the channel
    :return: type: <dictionary>, The dictionary contains the information of that youtube channel like channel_ID, Playlist_ID, channel_name fetched using youtube api
    '''

    video_desc = {}
    final_video_info = []

    try:
        request = youtube.videos().list(
        part = 'snippet,statistics,contentDetails',
        id = ",".join(video_list['video_ids'])
        )
        response = request.execute()

        video_desc = dict(
        channel_ID = [response['items'][i]['snippet']['channelId'] for i in range(len(response['items']))],
        video_ID = [response['items'][i]['id'] for i in range(len(response['items']))],
        video_published_date = [dt.strptime(response['items'][i]['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d") for i in range(len(response['items']))],
        video_title = [response['items'][i]['snippet']['title'] for i in range(len(response['items']))],
        video_views = [response['items'][i]['statistics']['viewCount'] for i in range(len(response['items']))],
        video_likes = [response['items'][i]['statistics']['likeCount'] for i in range(len(response['items']))],
        video_comments = [response['items'][i]['statistics']['commentCount'] for i in range(len(response['items']))],
        video_thumbnail = [response['items'][i]['snippet']['thumbnails']['high']['url'] for i in range(len(response['items']))],
        video_links = ["https://www.youtube.com/watch?v="+response['items'][i]['id'] for i in range(len(response['items']))]
        )
        
        final_video_info.append(video_desc)

        return final_video_info

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
