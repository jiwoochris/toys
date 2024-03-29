# Created or modified on May 2022
# Author: 임일
# Demographic 사용 추천

import numpy as np
import pandas as pd

# 데이터 읽어 오기 
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('data/u.user', sep='|', names=u_cols, encoding='latin-1')
i_cols = ['movie_id', 'title', 'release date', 'video release date', 'IMDB URL', 'unknown', 
          'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 
          'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 
          'Thriller', 'War', 'Western']
movies = pd.read_csv('data/u.item', sep='|', names=i_cols, encoding='latin-1')
r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv('data/u.data', sep='\t', names=r_cols, encoding='latin-1')

# timestamp 제거 
ratings = ratings.drop('timestamp', axis=1)
# movie ID와 title 빼고 다른 데이터 제거
movies = movies[['movie_id', 'title']]

# train, test set 분리
from sklearn.model_selection import train_test_split
x = ratings.copy()
y = ratings['user_id']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y)

# 정확도(RMSE)를 계산하는 함수
def RMSE(y_true, y_pred):
    return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2))

# 모델별 RMSE를 계산하는 함수 
def score(model):
    id_pairs = zip(x_test['user_id'], x_test['movie_id'])
    y_pred = np.array([model(user, movie) for (user, movie) in id_pairs])
    y_true = np.array(x_test['rating'])
    return RMSE(y_true, y_pred)

# train 데이터로 Full matrix 구하기 
rating_matrix = x_train.pivot(index='user_id', columns='movie_id', values='rating')

########## (1) 

# 전체 평균으로 예측치를 계산하는 기본 모델
def best_seller(user_id, movie_id):
    try:
        rating = train_mean[movie_id]
    except:
        rating = 3.0
    return rating

train_mean = x_train.groupby(['movie_id'])['rating'].mean()
print("best_seller: ", score(best_seller))

# Full matrix를 사용자 데이터와 merge
merged_ratings = pd.merge(x_train, users)
users = users.set_index('user_id')

# gender별 평점평균 계산
g_mean = merged_ratings[['movie_id', 'sex', 'rating']].groupby(['movie_id', 'sex'])['rating'].mean()

###### Gender기준 추천 ######
# gender별 평균을 예측치로 돌려주는 함수 
def cf_gender(user_id, movie_id):
    if movie_id in rating_matrix:
        gender = users.loc[user_id]['sex']
        if gender in g_mean[movie_id]:
            gender_rating = g_mean[movie_id][gender]
        else:
            gender_rating = 3.0
    else:
        gender_rating = 3.0
    return gender_rating

print("cf_gender: ", score(cf_gender))




##### 가설 1 #####

# 정보가 없는 영화에 3점 대신 모든 영화의 평균으로 대체
def best_seller_not3(user_id, movie_id):

    try:
        rating = train_mean[movie_id]
    except:
        rating = train_mean.mean()
    return rating

print("best_seller_not3: ", score(best_seller_not3))


##### 가설 2 #####

# 사용자별 평균 평점 계산
user_mean_rating = ratings.groupby('user_id')['rating'].mean()

# 전체 사용자의 평균평점 계산
overall_mean_rating = ratings['rating'].mean()

# user의 점수 주는 기준이 짠지 후한지 계산 (사용자별평균평점 - 전체 사용자의 평균평점)
user_rating_deviation = user_mean_rating - overall_mean_rating

# 평가기준 짠지 후한지를 고려해서 계산하는 기본 모델
def best_seller_with_deviation(user_id, movie_id):
    try:
        rating = train_mean[movie_id] + user_rating_deviation[user_id]
    except:
        rating = 3.0
    return rating

print("best_seller_with_deviation: ", score(best_seller_with_deviation))


# 전체 평균으로 예측치를 계산하는 기본 모델
def best_seller_with_deviation_not3(user_id, movie_id):
    try:
        rating = train_mean[movie_id] + user_rating_deviation[user_id]
    except:
        rating = train_mean.mean() + user_rating_deviation[user_id]
    return rating

print("best_seller_with_deviation_not3: ", score(best_seller_with_deviation_not3))