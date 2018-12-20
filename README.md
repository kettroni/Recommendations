# [create_XY.py:](https://github.com/sosma/recomendations/blob/master/src/create_XY.py)
Creates the X data and the y data

# [randomforest.py:](https://github.com/sosma/recomendations/blob/master/src/randomforest.py)
Creates the randomforest classifier and splits the data to train and test data, trains the classifier using the training data and saves the model to model/random_forest.joblib

# [recommendation.py:](https://github.com/sosma/recomendations/blob/master/src/recommendation.py)
This file contains a function 'recommend' which takes a user vector as a parameter and returns a predicted restaurant id by the classifier.
