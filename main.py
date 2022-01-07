
import datetime
from Playlist import *
from googleapiclient.discovery import build
from Google import create_service

CLIENT_SECRET_FILE = 'client_secret.json'
API = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

youtube = create_service(CLIENT_SECRET_FILE, API, API_VERSION, SCOPES)

def delete_old_videos():
    request = youtube.playlistItems().list(
        part = 'contentDetails', 
        playlistId = MY_PLAYLIST_ID,
        maxResults = 10
    )
    response = request.execute()

    playlist_items = response['items']

    for item in playlist_items:
        youtube.playlistItems().delete(id=item['id']).execute()

def add_today_videos():
    date = str(datetime.datetime.now())
    dt = date[:10] + "T00:00:00.000Z"

    request = youtube.search().list(
        part="id,snippet",
        channelId=MAGDALA_CHANNEL_ID,
        type='video',
        publishedAfter=dt,
        maxResults=10    
    )
    response = request.execute()

    videos_to_send = []
    keywords = ['Atardecer', 'Celebración']

    for i in range(len(response)):
        video_title = response['items'][i]['snippet']['title']
        
        if any(x in video_title for x in keywords):
            videos_to_send.append(response['items'][i])


    for video in videos_to_send:
        request = {
            'snippet': {
                'playlistId': MY_PLAYLIST_ID,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video['id']['videoId']  
                }
            }
        }

        youtube.playlistItems().insert(
            part='snippet',
            body = request
        ).execute()

def main():
    delete_old_videos()
    add_today_videos()

if __name__ == "__main__":
    main()