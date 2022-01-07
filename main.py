
from googleapiclient.discovery import build
from Google import create_service

CLIENT_SECRET_FILE = 'client_secret.json'
API = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

youtube = create_service(CLIENT_SECRET_FILE, API, API_VERSION, SCOPES)

my_playlist_id = 'PLfHkwilQ38SZ728xP0MoFPpq5FCo6uujk'


def delete_videos_my_playlist():
    response = youtube.playlistItems().list(
        part = 'contentDetails', 
        playlistId = my_playlist_id,
        maxResults = 10
    ).execute()

    playlistItems = response['items']

    for item in playlistItems:
        youtube.playlistItems().delete(id=item['id']).execute()

