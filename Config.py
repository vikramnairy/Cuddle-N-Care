import pyrebase

config = {
  "apiKey": "AIzaSyArIBtklBP7lAyTnbYPWu2KyRDrJIgwDLM",
  "authDomain": "cuddlencare-63e0f.firebaseapp.com",
  "databaseURL":"https://cuddlencare-63e0f.firebaseio.com",
  "projectId": "cuddlencare-63e0f",
  "storageBucket": "cuddlencare-63e0f.appspot.com",
  "messagingSenderId": "93970327536",
  "appId": "1:93970327536:web:5ce1a8cef4d949a986df35",
  "measurementId": "G-27D6D6MV0W",
}

firebase = pyrebase.initialize_app(config)
db=firebase.database()


