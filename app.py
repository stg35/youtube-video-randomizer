import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

playlistsID = ['PLh6dVTO7f4FZvh7NMJ3iYWlA--kK4yjad', 'PLrxF2hSiV3wCK09ElXEyXrMeiOf-e4zLC']

videos = []

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "CLIENT_SECRET_FILE.json"

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    for ID in playlistsID:
        request_playlist = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=3,
            playlistId=ID
        )
        response_playlist = request_playlist.execute()

        for item in response_playlist['items']:
            videoID = item['contentDetails']['videoId']
            request_video = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=videoID
            )
            response_video = request_video.execute()
            print(videoID)
            if response_video['items']:
                publishedAt = response_video['items'][0]['snippet']['publishedAt']
                title = response_video['items'][0]['snippet']['title']
                duration = response_video['items'][0]['contentDetails']['duration']
                p1 = duration.find('T')
                p2 = duration.find('H')
                p3 = duration.find('M')
                p4 = duration.find('S')
                h = int(duration[p1+1:p2])
                m = int(duration[p2+1:p3])
                s = int(duration[p3+1:p4])
                duration = h*3600 + m*60 + s
                videos.append({'videoID': videoID, 'publishedAt': publishedAt, 'title': title, 'duration': duration})

    print(videos)

if __name__ == "__main__":
    main()