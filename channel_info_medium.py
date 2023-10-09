# import logging
import googleapiclient.errors

# logging.basicConfig(filename="youtube_scarpping_logs.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

def get_video_details(youtube, video_dict):

    '''
    This fuction is used to provide the video info of the channel by passing the video IDs of the videos using youtube api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param youtube_name: type: <String>, It is the username of the channel
    :return: type: <dictionary>, The dictionary contains the information of that youtube channel like channel_ID, Playlist_ID, channel_name fetched using youtube api
    '''

    try:
            video_info = []
            request = youtube.videos().list(
                    part = 'snippet,statistics,contentDetails',
                    id = ",".join(video_dict['video_ids'][:50])
            )
            response = request.execute()
            video_info.extend(response["items"])


            request1 = youtube.videos().list(
                    part = 'snippet,statistics,contentDetails',
                    id = ",".join(video_dict['video_ids'][50:])
            )
            response1 = request1.execute()
            video_info.extend(response1["items"])          

            return video_info

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
