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
            if response_video['items']:
                publishedAt = response_video['items'][0]['snippet']['publishedAt']
                title = response_video['items'][0]['snippet']['title']
                duration = response_video['items'][0]['contentDetails']['duration']
                for i in range(len(duration)):
                    if duration[i] == 'H':
                        point = i
                        while duration[i] != 'T':
                            i -= 1
                        h = int(duration[i+1:point])
                    elif duration[i] == 'M':
                        point = i
                        while (duration[i] != 'H') and (duration[i] != 'T'):
                            i-=1
                        m = int(duration[i+1:point])
                    elif duration[i] == 'S':
                        point = i
                        while (duration[i] != 'M') and (duration[i] != 'T') and (duration[i] != 'H'):
                            i-=1
                        s = int(duration[i+1:point])
                duration = h*3600 + m*60 + s
                viewCount = response_video['items'][0]['statistics']['viewCount']
                likeCount = response_video['items'][0]['statistics']['likeCount']
                dislikeCount = response_video['items'][0]['statistics']['dislikeCount']
                commentCount = response_video['items'][0]['statistics']['commentCount']
                tags = response_video['items'][0]['snippet']['tags']
                videos.append({'videoID': videoID, 'publishedAt': publishedAt, 'title': title,
                               'duration': duration, 'viewCount': viewCount, 'likeCount': likeCount,
                               'dislikeCount': dislikeCount, 'commentCount': commentCount, 'tags': tags,
                               'playlistID': ID})

    print(videos)

if __name__ == "__main__":
    main()