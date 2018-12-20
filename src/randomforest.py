import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

PATH = 'data/'
df_X = pd.read_csv(PATH + 'dataX.csv')
df_y = pd.read_csv(PATH + 'dataY.csv')
tempY = df_y.values.tolist()
X = df_X.values.tolist()
y = list(map(lambda x: x[0], tempY))


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42)

X_train, y_train = make_classification()

clf = RandomForestClassifier()
clf.fit(X, y)

print(clf.score(X_test, y_test))

from sklearn.externals import joblib
joblib.dump(clf, 'model/random_forest.joblib')
