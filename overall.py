#PYREBASE FIREBASE
from kivy.properties import StringProperty
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyrebase
import datetime

location = StringProperty()
username = StringProperty
heading = "HILTON STEEL AND CEMENT POS"

cred = credentials.Certificate('privatekey.json')

dbs = firebase_admin.db

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cocabpos-e5199.firebaseio.com/'
})

ref = db.reference()


firebaseconfig = {
    "apiKey": "AIzaSyDGsXv0wa7Fc4irPi3MX_uWTIfuWHeEIzU",
    "authDomain": "projectId.firebaseapp.com",
    "databaseURL": "https://cocabpos-e5199.firebaseio.com/",
    "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(firebaseconfig)
auth = firebase.auth()

db = firebase.database()


now = datetime.datetime.now()
hour = str(now.hour)
minute = str(now.minute)
second = str(now.second)
combined_date = str(hour) + str(minute) + str(second)
today = str(datetime.datetime.today().date())
