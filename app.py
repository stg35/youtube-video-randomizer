import requests
import csv
from secret_data import API_KEY
from db import removeCollection, addVideo
import os

# def csv_writer(data, path):
#     with open(path, 'w+', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         for line in data:
#             writer.writerow(line)

def csv_remove(path):
    with open(path, 'w+', newline='') as csv_file:
        print('csv was deleted.')

def csv_addRow(path, data):
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)

def loading(i, n):
    return round(i/n, 2) * 100

def parsedDuration(duration):
    h = 0
    m = 0
    s = 0
    for i in range(len(duration)):
        if duration[i] == 'H':
            point = i
            while duration[i] != 'T':
                i -= 1
            h = int(duration[i + 1:point])
        elif duration[i] == 'M':
            point = i
            while (duration[i] != 'H') and (duration[i] != 'T'):
                i -= 1
            m = int(duration[i + 1:point])
        elif duration[i] == 'S':
            point = i
            while (duration[i] != 'M') and (duration[i] != 'T') and (duration[i] != 'H'):
                i -= 1
            s = int(duration[i + 1:point])
    return h*3600 + m*60 + s

playlistsID = 'UUSPd93is2UQsd_jZ6yHBfqQ'
videos = []
data = ['id title tags description views likes dislikes'.split()]
totalResults = 3338
path = 'videos_metadata.csv'

def main():
    removeCollection()
    csv_remove(path)
    k = 0
    for page in range(1, totalResults+1):
        if page == 1:
            request_playlist = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={0}&key={1}'.format(playlistsID, API_KEY))
        else:
            request_playlist = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?pageToken={2}&part=snippet%2CcontentDetails&maxResults=50&playlistId={0}&key={1}'.format(playlistsID, API_KEY, nextPageToken))
        response_playlist = request_playlist.json()
        for item in response_playlist['items']:
            videoID = item['contentDetails']['videoId']
            request_video = requests.get('https://www.googleapis.com/youtube/v3/videos?id={0}&key={1}&part=snippet,contentDetails,statistics,status'.format(videoID, API_KEY))
            response_video = request_video.json()
            if response_video['items']:
                try:
                    publishedAt = response_video['items'][0]['snippet']['publishedAt']
                    title = response_video['items'][0]['snippet']['title']
                    description = response_video['items'][0]['snippet']['description']
                    duration = parsedDuration(response_video['items'][0]['contentDetails']['duration'])
                    viewCount = response_video['items'][0]['statistics']['viewCount']
                    likeCount = response_video['items'][0]['statistics']['likeCount']
                    dislikeCount = response_video['items'][0]['statistics']['dislikeCount']
                    commentCount = response_video['items'][0]['statistics']['commentCount']
                    try:
                        tags = response_video['items'][0]['snippet']['tags']
                    except:
                        tags = ''
                    addVideo({'_id': k, 'videoID': videoID, 'publishedAt': publishedAt, 'title': title,
                                   'description': description , 'duration': duration, 'viewCount': viewCount,
                                   'likeCount': likeCount, 'dislikeCount': dislikeCount, 'commentCount': commentCount,
                                   'tags': tags, 'playlistID': playlistsID})
                    csv_addRow(path, [videoID, title, ','.join(tags), description, viewCount, likeCount, dislikeCount])
                except:
                    print(videoID)
                ln = 0
                if loading(k, totalResults) > ln:
                    ln = loading(k, totalResults)
                    os.system('clear')
                    print(int(ln), '%', sep='')
                k += 1
                try:
                    nextPageToken = response_playlist['nextPageToken']
                except:
                    print('All data uploaded.')

if __name__ == "__main__":
    main()
