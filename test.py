import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from hmmlearn import hmm
import operator
import os
import pickle
'''
dataset = pd.read_csv("Dataset/bat.csv", usecols = ['name_x', 'runs_x', 'balls', 'strike_rate', 'fours', 'sixes', 'how_out', 'run_rate'])

le1 = LabelEncoder()
le2 = LabelEncoder()
scaler = StandardScaler()

dataset['name_x'] = pd.Series(le1.fit_transform(dataset['name_x'].astype(str)))
dataset['how_out'] = pd.Series(le2.fit_transform(dataset['how_out'].astype(str)))
dataset = dataset.values

X = dataset[:,0:dataset.shape[1]-1]
Y = dataset[:,dataset.shape[1]-1]

X = scaler.fit_transform(X)
print(X.shape)
print(Y.shape)

if os.path.exists("model/bat"):
    with open('model/bat', 'rb') as file:
        model = pickle.load(file)
    file.close()
else:
    model = hmm.GaussianHMM(10, "full", n_iter=500)
    model.fit(X)
    with open('model/bat', 'wb') as file:
        pickle.dump(model, file)
    file.close()
    

    
testData = pd.read_csv("Dataset/test_bat.csv", usecols = ['name_x', 'runs_x', 'balls', 'strike_rate', 'fours', 'sixes', 'how_out'])
player = testData['name_x']
testData['name_x'] = pd.Series(le1.transform(testData['name_x'].astype(str)))
testData['how_out'] = pd.Series(le2.transform(testData['how_out'].astype(str)))
testData = testData.values
X = scaler.transform(testData)

performance = []

predict = model.predict(X)
print(model.score(X))

selected = []
for i in range(len(predict)):
    if player[i] not in selected:
        selected.append(player[i])
        performance.append([player[i], predict[i]])
performance.sort(key = operator.itemgetter(1), reverse = True)
for i in range(0,15):
    print(performance[i])
===============================================
'''

dataset = pd.read_csv("Dataset/ball.csv", usecols = ['name_x', 'run_conceded', 'maidens', 'wickets', 'overs', 'economy', 'wides', 'no_balls', 'fours',
                                                     'sixes', 'zeros', 'runs', 'over', 'run_rate'])

dataset.fillna(0, inplace = True)
le3 = LabelEncoder()
scaler1 = StandardScaler()

dataset['name_x'] = pd.Series(le3.fit_transform(dataset['name_x'].astype(str)))
X = dataset.values

X = scaler1.fit_transform(X)
print(X.shape)


if os.path.exists("model/ball"):
    with open('model/ball', 'rb') as file:
        model = pickle.load(file)
    file.close()
else:
    model = hmm.GaussianHMM(10, "full", n_iter=5000)
    model.fit(X)
    with open('model/ball', 'wb') as file:
        pickle.dump(model, file)
    file.close()
    

    
testData = pd.read_csv("Dataset/test_ball.csv", usecols = ['name_x', 'run_conceded', 'maidens', 'wickets', 'overs', 'economy', 'wides', 'no_balls', 'fours',
                                                     'sixes', 'zeros', 'runs', 'over', 'run_rate'])
testData.fillna(0, inplace = True)
player = testData['name_x']
testData['name_x'] = pd.Series(le3.transform(testData['name_x'].astype(str)))
testData = testData.values
X = scaler1.transform(testData)

performance = []

predict = model.predict(X)
print(model.score(X))

selected = []
for i in range(len(predict)):
    if player[i] not in selected:
        selected.append(player[i])
        performance.append([player[i], predict[i]])
performance.sort(key = operator.itemgetter(1), reverse = True)
for i in range(0,15):
    print(performance[i])




    
