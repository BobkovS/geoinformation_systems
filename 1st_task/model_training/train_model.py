import os
import pickle

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv(os.path.join('..', 'data', 'data.csv'))
data = data[np.isfinite(data['poly_shapes_count'])]

list_of_levels = list(range(200))
for index, element in enumerate(list_of_levels):
    list_of_levels[index] = element.__str__()
list_of_levels.append(np.nan)

drop_ids = []
for index, row in data.iterrows():
    if row['building:levels'] not in list_of_levels:
        drop_ids.append(index)

data = data.drop(drop_ids)
data = data.fillna(0)

test, train = data[data.building == 'yes'], data[data.building != 'yes']
test, train = test.reset_index(drop=True), train.reset_index(drop=True)

dv = LabelEncoder()
dv.fit(data.building)

train.building = dv.transform(train.building)
test.building = dv.transform(test.building)
train = train.astype('float')
test = test.astype('float')

train_x = train.drop(['building'], axis=1)
train_y = train.building
test_x = test.drop(['building'], axis=1)

clf = LogisticRegression(verbose=True, solver='lbfgs', n_jobs=-1)
clf.fit(train_x, train_y)

pickle.dump(clf, open(os.path.join('..', 'data', 'model.pkl'), 'wb'))
pickle.dump(dv, open(os.path.join('..', 'data', 'encoder.pkl'), 'wb'))
