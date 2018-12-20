import pandas as pd
import pymysql
from sqlalchemy import create_engine
from pathlib import Path
import os.path
import json

hostname = 'SOME HOST NAME'
engine = create_engine('CREATE_ENGINE')

query =  """SELECT * FROM bookings
 LEFT JOIN contacts ON bookings.contact_id = contacts.id
 LEFT JOIN restaurants ON bookings.restaurant_id = restaurants.id
 LEFT JOIN atmospheres_restaurants ON bookings.restaurant_id = atmospheres_restaurants.restaurant_id
 LEFT JOIN atmospheres ON atmospheres_restaurants.atmosphere_id = atmospheres.id
 WHERE bookings.booking_date > '2014-01-01' and bookings.booking_date < '2018-09-23'
 AND contacts.email_address LIKE '%%lavas%%'
 and contacts.firstname = 'Ilkka' and contacts.lastname = 'Lavas' """

# yleiset arvostelut ravintoloista
# - restaurantid, ravintola ja ravintolan ratings -> ehkä keskiarvo tästä?

my_file = 'opinions.json'
if os.path.isfile(my_file):
  #file exists, read it
  print ('file exists, read df from json in it')
  with open(my_file) as tmp_file:
    opinions_json = json.load(tmp_file)
  #converting json dataset from dictionary to dataframe
  opinions_df = pd.DataFrame.from_dict(opinions_json, orient='index')
  opinions_df.reset_index(level=0, inplace=True)
else:
  #file not found, let's create one from sql
  query = """SELECT * FROM tableonline.opinions"""
  print (query)
  opinions_df = pd.read_sql_query(query, engine)
  opinions_df.to_json(my_file)


# jokaiselle ravintolalle atmospheret
# restaurantid ja atmosphere.name

my_file = 'restaurant_atmosphere.json'
if os.path.isfile(my_file):
  #file exists, read it
  print ('file contact_opinions exists, read df from json in it')
  with open(my_file) as tmp_file:
    restaurant_atmosphere_json = json.load(tmp_file)
  #converting json dataset from dictionary to dataframe
  restaurant_atmosphere_df = pd.DataFrame.from_dict(restaurant_atmosphere_json, orient='index')
  restaurant_atmosphere_df.reset_index(level=0, inplace=True)
else:
  #file not found, let's create one from sql
  query = """SELECT tableonline.restaurants.id, tableonline.atmospheres.id as atmosphereid, tableonline.atmospheres.name as atmospherename FROM tableonline.restaurants
   INNER JOIN atmospheres_restaurants ON atmospheres_restaurants.restaurant_id = restaurants.id
   INNER JOIN atmospheres ON atmospheres_restaurants.atmosphere_id = atmospheres.id"""
  print (query)
  restaurant_atmosphere_df = pd.read_sql_query(query, engine)
  restaurant_atmosphere_df.to_json(my_file)


# jokaiselle henkiölle omat ravintolan arvostelut
# - restaurantid contacts.id opinions.rate
# distinct = email

my_file = 'contact_opinions.json'
if os.path.isfile(my_file):
  #file exists, read it
  print ('file contact_opinions exists, read df from json in it')
  with open(my_file) as tmp_file:
    contacts_opinions_json = json.load(tmp_file)
  #converting json dataset from dictionary to dataframe
  contacts_opinions_df = pd.DataFrame.from_dict(contacts_opinions_json, orient='index')
  contacts_opinions_df.reset_index(level=0, inplace=True)
else:
  #file not found, let's create one from sql
  query = """SELECT opinions.id as opinionsid, opinions.restaurant_id, opinion_date, restaurants.name as restaurantname,
   restaurants.city, bookings.booking_date, bookings.booking_time, bookings.user_firstname, bookings.user_lastname,
   bookings.contact_id, bookings.user_phone, bookings.user_email_address, contacts.fixed_phone, contacts.mobile_phone
    FROM tableonline.opinions
   INNER JOIN restaurants ON opinions.restaurant_id = restaurants.id
   INNER JOIN bookings ON bookings.id = opinions.booking_id
   INNER JOIN contacts ON contacts.id = bookings.contact_id"""
  print (query)
  contacts_opinions_df = pd.read_sql_query(query, engine)
  contacts_opinions_df.to_json(my_file)




# jokaiselle ravintolalle cookings
# ravintolaid , cookings.name


my_file = 'cookings.json'
if os.path.isfile(my_file):
  #file exists, read it
  print ('file contact_opinions exists, read df from json in it')
  with open(my_file) as tmp_file:
    cookings_json = json.load(tmp_file)
  #converting json dataset from dictionary to dataframe
  cookings_df = pd.DataFrame.from_dict(cookings_json, orient='index')
  cookings_df.reset_index(level=0, inplace=True)
else:
  #file not found, let's create one from sql
  query = """SELECT cookings.id, cookings.name as coonkingsname, cookings.category, cookings.key, restaurants.id as restaurantid, restaurants.name as restaurantname FROM cookings
   INNER JOIN cookings_restaurants ON cookings_restaurants.restaurant_id = cookings.id
   INNER JOIN restaurants ON cookings_restaurants.restaurant_id = restaurants.id"""
  print (query)
  cookings_df = pd.read_sql_query(query, engine)
  cookings_df.to_json(my_file)


# jokaiselle henkilokohtainen rating per ravintola
# ratings  ravintolaid, email_address, firstname, lastname, fixed_phone, mobile_phone, rate

my_file = 'restaurant_contact_rating.json'
if os.path.isfile(my_file):
  #file exists, read it
  print ('file contact_opinions exists, read df from json in it')
  with open(my_file) as tmp_file:
    restaurant_contact_rating_json = json.load(tmp_file)
  #converting json dataset from dictionary to dataframe
  restaurant_contact_rating_df = pd.DataFrame.from_dict(restaurant_contact_rating_json, orient='index')
  restaurant_contact_rating_df.reset_index(level=0, inplace=True)
else:
  #file not found, let's create one from sql
  query = """SELECT tableonline.restaurants.id as restaurantid,contacts.email_address,contacts.firstname,contacts.lastname,contacts.fixed_phone,contacts.mobile_phone,opinions.rate FROM tableonline.opinions
   INNER JOIN restaurants ON opinions.restaurant_id = restaurants.id
   INNER JOIN bookings ON bookings.id = opinions.booking_id
   INNER JOIN contacts ON contacts.id = bookings.contact_id"""
  print (query)
  restaurant_contact_rating_df = pd.read_sql_query(query, engine)
  restaurant_contact_rating_df.to_json(my_file)
