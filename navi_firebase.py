import pyrebase
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class firebaseCRUD:

    cred = credentials.Certificate("joe-mlidnd-firebase-adminsdk-d5dy3-91d9301d1e.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://joe-mlidnd.firebaseio.com'})

    config = {
        "apiKey": "AIzaSyBJYcE3HXN7CZaV9qBflNJwMgt6q2vQJ1g",
        "authDomain": "joe-mlidnd.firebaseapp.com",
        "databaseURL": "https://joe-mlidnd.firebaseio.com",
        "projectId": "joe-mlidnd",
        "storageBucket": "joe-mlidnd.appspot.com",
    }

    firebase = pyrebase.initialize_app(config)

    auth = firebase.auth()

    user = auth.sign_in_with_email_and_password("chrischan0802@gmail.com", "123456")

    storage = firebase.storage()

    db = firebase.database()

          
    def addNewNavigation(self,na):      
        na = {
            "origins": na["origins"],
            "destination": na['destination'],
            "description": na['description']
        }
        navi_name = na['origins']+"-to-"+na['destination']
        self.db.child("navigation").child('building').child(navi_name).set(na)
        print("successfully")

    def retrieveDescription(self):
        naviDes = {}
        naviDes = self.db.child("navigation").get("building").get()
        #for x in naviDes.each():
         #     d = {}
          #    for item in x.val().values():
           #       d = item
        return naviDes.val()
   
    def getNaviName(self):
        ref = db.reference('navigation/building')
        description = ref.get()
        #print(sup)
        navis = {}
        for key, val in description.items():   
             navis = key
             #print(navis)
        return description
     
    def getNavidetail(self,naviName):
        ref = db.reference('navigation/building')
        description = ref.get()
        na = {}
        for key, val in description.items():
            if key == naviName:
               na['naviName'] = key
               for key,val in val.items():

                if key == "description":
                  na['description'] = val

                if key == "origins":
                  na['origins'] = val

                if key == "destination":
                    na['description'] = val
        return na
     
    def addImage():
        storage = firebase.storage()
        storage.child("images/blockA.jpg").put("sad.jpg")

    def getFaUrl(self,filename):
        fileName = filename+".jpg"
        hihi =  storage.child("images/"+fileName).get_url()
        return hihi