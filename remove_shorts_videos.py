# import logging
import googleapiclient.errors

# logging.basicConfig(filename="youtube_scarpping_logs.log", level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

def remove_shorts_videos(youtube, video_info, video_dict, channel_id):

    '''
    This fuction is used to remove the youtube shorts and collect video information only for long videos using youtube api
    :param youtube: <googleapiclient.discovery.Resource object at 0x000001A0E2A2BB38>
    :param youtube_name: type: <String>, It is the username of the channel
    :return: type: <dictionary>, The dictionary contains the information of that youtube channel like channel_ID, Playlist_ID, channel_name fetched using youtube api
    '''

    try:
        video_duration_seconds = []
        short_video_duration_threshold = 120
        non_short_videos = []

        for i in range(len(video_info)):
            if "S" in video_info[i]['contentDetails']['duration'] and "M" not in video_info[i]['contentDetails']['duration']:
                video_duration_seconds.append(int(video_info[i]['contentDetails']['duration'].split("T")[-1].split("S")[0]))

            if "H" in video_info[i]['contentDetails']['duration']:
                video_duration_seconds.append(int(video_info[i]['contentDetails']['duration'].split("T")[-1].split("H")[0]) * 3600)

            if "M" in video_info[i]['contentDetails']['duration'] and "H" not in video_info[i]['contentDetails']['duration']:
                video_duration_seconds.append(int(video_info[i]['contentDetails']['duration'].split("T")[-1].split("M")[0]) * 60)


        no_of_videos = len(non_short_videos)

        for i, duration in enumerate(video_duration_seconds):
            if no_of_videos >= 50:
                break

            if duration > short_video_duration_threshold:
                non_short_videos.append(video_dict['video_ids'][i])
                no_of_videos += 1

        channel_video_info = dict(channel_id = channel_id['channel_id'], video_ids = non_short_videos)

        return channel_video_info

    except googleapiclient.errors.HttpError as e:
        status_code = e.resp.status
        error_message = e.content.decode("utf-8")
        print(f"HTTP status code: {status_code}")
        print(f"Error message: {error_message}")



    if __name__=='__main__':
        from googleapiclient.discovery import build
        DEVELOPER_KEY = "AIzaSyAaeo-q3kZLtB8G6QKCvQoz6eB3J-oN2Cw"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)   
