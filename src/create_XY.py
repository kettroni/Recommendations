import pandas as pd
import numpy as np
PATH = 'data/'
# id | coonkingsname | key | restaurantid | restaurantname
df_cookings = pd.read_json(PATH + 'cookings.json')

# id | restaurant_id | my_table_id | opinion_date | rate | title | comment | state (if valitaded or not) | booking_id (can be none)
df_opinions = pd.read_json(PATH + 'opinions.json')

# id | atmosphereid | atmospherename
df_restaurant_atmosphere = pd.read_json(PATH + 'restaurant_atmosphere.json')

# restaurantid | email_address | firstname | lastname | fixed_phone | mobile_phone | rate
df_restaurant_contact_rating = pd.read_json(PATH + 'restaurant_contact_rating.json') # DELETED DUE PRIVACY ISSUES (contains email)

# opinionsid | restaurant_id | opinion_date | restaurantname | city | booking_date | booking_time
# | user_firstname | user_lastname | contact_id | user_phone | user_email_address | fixed_phone | mobile_phone
df_contact_opinions = pd.read_json(PATH + 'contact_opinions.json') # DELETED DUE PRIVACY ISSUES (contains email)

all_atmos = df_restaurant_atmosphere.atmospherename.unique()
all_cookings = df_cookings.coonkingsname.unique()

# restaurantid -> [atmosphere]
restaurant_atmos = {}
restaurant_atmos_ids = df_restaurant_atmosphere.id.unique()

restaurant_cookings = {}
restaurant_cookings_ids = df_cookings.restaurantid.unique()

restaurant_atmos_ids.sort()
restaurant_cookings_ids.sort()

for res_id in restaurant_atmos_ids:
    temp_df = df_restaurant_atmosphere[df_restaurant_atmosphere['id'] == res_id].drop_duplicates()
    temp_list = []
    for index, row in temp_df.iterrows():
        temp_list.append(row['atmospherename'])
    restaurant_atmos[res_id] = temp_list

for res_id in restaurant_cookings_ids:
    temp_df = df_cookings[df_cookings['restaurantid'] == res_id].drop_duplicates()
    temp_list = []
    for index, row in temp_df.iterrows():
        temp_list.append(row['coonkingsname'])
    restaurant_cookings[res_id] = temp_list

# Rating converge from string to 'weight'
def transform_rating(number):
    if number >= 4.5:
        return 2
    if number >= 3.5:
        return 1
    if number >= 2.5:
        return 0
    if number >= 1.5:
        return -1
    if number >= 0.5:
        return -2
    return 0

def get_opinions(email):
    df = df_restaurant_contact_rating
    df_p = df[df['email_address'] == email]
    res_ids = df.restaurantid.unique()
    res_ids.sort()
    bestrest = []
    opinions = {}
    for id in res_ids:
        opinions[id] = ''
    for res_id in res_ids:
        for index, row in df_p[df_p['restaurantid'] == res_id].iterrows():
            opinions[res_id] = row['rate']
            if row['rate'] >= 4:
                bestrest.append(res_id)
            break
    return [opinions, bestrest]


def id_in_atmos(id):
    return id in restaurant_atmos

def id_in_cookings(id):
    return id in restaurant_cookings

def create_user(email):

    # Counting user specific atmosphere, cookings amounts. Set everything to 0
    user_atmoscooking_amounts = {}
    for atmos in all_atmos:
        user_atmoscooking_amounts[atmos] = 0

    for cookings in all_cookings:
        user_atmoscooking_amounts[cookings] = 0

    # Counting user specific atmosphere, cookings value. Set everything to 0
    user_atmoscooking_val = {}
    for atmos in all_atmos:
        user_atmoscooking_val[atmos] = 0

    for cookings in all_cookings:
        user_atmoscooking_val[cookings] = 0


    user_ratings, user_bestrest = get_opinions(email)
    user = np.array([])
    for restaurant_id, rating in user_ratings.items():
        # If user hasn't given a rating to a restaurant
        if id_in_atmos(restaurant_id) and id_in_cookings(restaurant_id):
            if rating == '':
                pass
            else:
                for atmos in restaurant_atmos[restaurant_id]:
                    # Update each atmosphere
                    user_atmoscooking_amounts[atmos] += 1
                    user_atmoscooking_val[atmos] += float(rating)
                for cooking in restaurant_cookings[restaurant_id]:
                    # Update each cooking
                    user_atmoscooking_amounts[cooking] += 1
                    user_atmoscooking_val[cooking] += float(rating)

    for atmoscooking, atmoscooking_val in user_atmoscooking_val.items():
        # Add weight to user vector by counting mean of ratings for specific atmoscooking and then transforming it.

        divider = user_atmoscooking_amounts[atmoscooking]
        if divider == 0:
            divider = 1
        user = np.append(user, [(atmoscooking_val / divider)])

    return [user, user_bestrest]

users = df_restaurant_contact_rating.email_address.unique()
users = users[users != np.array(None)]


def create_XY():
    tempX = []
    tempY = []
    i = len(users)
    for email in users:
        user, bestrest = create_user(email)
        for rest in bestrest:
            tempX.append(user)
            tempY.append(rest)


        print(i)
        i-=1

    df = pd.DataFrame(tempX)
    df2 = pd.DataFrame(tempY)
    df.to_csv('data/dataX.csv', index=False)
    df2.to_csv('data/dataY.csv', index=False)


#create_XY()
def get_restaurantname(id):
    return (df_cookings[df_cookings['restaurantid'] == id].restaurantname.unique()[0])
