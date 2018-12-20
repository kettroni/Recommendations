# [create_XY.py:](https://github.com/kettroni/recommendations/blob/master/src/create_XY.py)
Creates the X data and the y data

# [randomforest.py:](https://github.com/kettroni/recommendations/blob/master/src/randomforest.py)
Creates the randomforest classifier and splits the data to train and test data, trains the classifier using the training data and saves the model to model/random_forest.joblib

# [recommendation.py:](https://github.com/kettroni/recomendations/blob/master/src/recommendation.py)
This file contains a function 'recommend' which takes a user vector as a parameter and returns a predicted restaurant id by the classifier.

# [tableonline.py:](https://github.com/kettroni/recommendations/blob/master/data/tableonline.py)
Creates JSON files from the SQL Database. They are then used for creating the XY Data.
