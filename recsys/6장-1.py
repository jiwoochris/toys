# Created or modified on May 2022
# Author: 임일
# Surprise - 기본

import numpy as np
import pandas as pd

# 필요한 Surprise 알고리즘 불러오기
from surprise import BaselineOnly 
from surprise import KNNWithMeans
from surprise import SVD
from surprise import SVDpp
from surprise import NMF
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split

# MovieLens 100K 데이터 불러오기
data = Dataset.load_builtin('ml-100k')

# Train/Test 분리 
trainset, testset = train_test_split(data, test_size=0.25)

##### (1)

# 정확도 계산 
algo = KNNWithMeans()
algo.fit(trainset)
predictions = algo.test(testset)
accuracy.rmse(predictions)


# Build the full trainset
trainset = data.build_full_trainset()

# Iterate over the trainset to print some data
for uid, iid, rating in trainset.all_ratings():
    print(f"User: {uid}, Item: {iid}, Rating: {rating}")