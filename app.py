import requests
from secret_data import API_KEY

playlistsID = ['PLh6dVTO7f4FZvh7NMJ3iYWlA--kK4yjad', 'PLrxF2hSiV3wCK09ElXEyXrMeiOf-e4zLC']

videos = []

def main():

    for ID in playlistsID:
        #maxResults = 3
        request_playlist = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=3&playlistId={0}&key={1}'.format(ID, API_KEY))
        response_playlist = request_playlist.json()
        for item in response_playlist['items']:
            videoID = item['contentDetails']['videoId']
            request_video = requests.get('https://www.googleapis.com/youtube/v3/videos?id={0}&key={1}&part=snippet,contentDetails,statistics'.format(videoID, API_KEY))
            response_video = request_video.json()
            print(videoID)
            if response_video['items']:
                publishedAt = response_video['items'][0]['snippet']['publishedAt']
                title = response_video['items'][0]['snippet']['title']
                duration = response_video['items'][0]['contentDetails']['duration']
                # p1 = duration.find('T')
                # p2 = duration.find('H')
                # p3 = duration.find('M')
                # p4 = duration.find('S')
                # h = int(duration[p1+1:p2])
                # m = int(duration[p2+1:p3])
                # s = int(duration[p3+1:p4])
                # duration = h*3600 + m*60 + s
                videos.append({'videoID': videoID, 'publishedAt': publishedAt, 'title': title, 'duration': duration})

    print(videos)

if __name__ == "__main__":
    main()