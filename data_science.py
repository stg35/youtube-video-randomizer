import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import norm
import math

def rating(pos, n, confidence):
    if n == 0:
        return 0
    z = norm.ppf(1-(1-confidence)/2)
    phat = 1.0*pos/n
    return (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

videos = pd.read_csv('videos_metadata.csv')
tfidf = TfidfVectorizer()
videos['all_data'] = videos['title']+','+videos['tags']+','+videos['description']
videos['all_data'] = videos['all_data'].fillna('')
overview_matrix = tfidf.fit_transform(videos['all_data'])
similarity_matrix = cosine_similarity(overview_matrix,overview_matrix)
mapping = pd.Series(videos.index,index = videos['id'])
videos['ratings'] = [rating(videos['likes'][i].item(),
                            videos['likes'][i].item()+videos['dislikes'][i].item(), 0.95)
                     for i in range(len(videos))]

def next_video(id, like=True):
    video_index = mapping[id]
    similarity_score = list(enumerate(similarity_matrix[video_index]))
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    kfs = [i[0] for i in similarity_score]
    if like:
        for i in kfs:
            if videos['ratings'][i] > 0.9:
                return videos['id'][i]
    else:
        for i in reversed(kfs):
            if videos['ratings'][i] > 0.9:
                return videos['id'][i]