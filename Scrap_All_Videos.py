# import logging
import googleapiclient.errors


# logging.basicConfig(filename="youtube_scarpping_logs.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

def get_all_video_ID(youtube, playlistid):

    '''
    This fuction is used to provide all the video IDs for all the videos uploaded on the channel by passing the playlist ID of uploaded playlist using youtube api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param youtube_name: type: <String>, It is the playlist ID of the playlist
    :return: type: <dictionary>, The dictionary contains the information of that youtube channel like channel_ID, Playlist_ID, channel_name fetched using youtube api
    '''
    
    try:
        video_details = []
        video_ids = []
        request_video_ID = youtube.playlistItems().list(
            part="contentDetails,snippet",
            maxResults=50,
            playlistId = playlistid,
        )

        response = request_video_ID.execute()
        video_details.extend(response["items"])

        while "nextPageToken" in response:
                nextPageToken = response["nextPageToken"]
                request = youtube.playlistItems().list(
                    part="contentDetails,snippet",
                    maxResults=50,
                    playlistId = playlistid,
                    pageToken=nextPageToken,
                )
                response = request.execute()
                video_details.extend(response["items"])
        
        for i in range(len(video_details)):
            video_ids.append(video_details[i]['contentDetails']['videoId'])

        return dict(channel_id = playlistid,
                    video_ids = video_ids[:100])
        
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