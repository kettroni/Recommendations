import numpy as np
import pandas as pd
from sklearn.externals import joblib
from create_XY import create_user, get_restaurantname

def recommend(user):
    user = user.reshape(1, -1)
    clf = joblib.load('model/random_forestV2.joblib')
    return clf.predict(user)[0]

user = create_user('GIVE HERE AN EXAMPLE EMAIL')[0]
recommendation = recommend(user)
print(get_restaurantname(recommendation))
