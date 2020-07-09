import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

videos = pd.read_csv('videos_metadata.csv')
print(videos['tags'][0])
tfidf = TfidfVectorizer()
videos['tags'] = videos['tags'].fillna('')
#Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
overview_matrix = tfidf.fit_transform(videos['tags'])
#Output the shape of tfidf_matrix
print(overview_matrix.shape)
similarity_matrix = linear_kernel(overview_matrix,overview_matrix)
print(similarity_matrix)
#movies index mapping
mapping = pd.Series(videos.index,index = videos['title'])
print(mapping)

def recommend_videos_based_on_tags(video_input):
    video_index = mapping[video_input]
    #get similarity values with other movies
    #similarity_score is the list of index and similarity matrix
    similarity_score = list(enumerate(similarity_matrix[video_index]))
    #sort in descending order the similarity score of movie inputted with all the other movies
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    # Get the scores of the 15 most similar movies. Ignore the first movie.
    similarity_score = similarity_score[1:15]
    #return movie names using the mapping series
    video_indices = [i[0] for i in similarity_score]
    return videos['title'].iloc[video_indices]

print('--------------------------')
#the 15 most similar videos
print(recommend_videos_based_on_tags('Римское право — курс Александра Марея и Дмитрия Дождева / ПостНаука'))