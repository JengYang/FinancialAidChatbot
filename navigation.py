
import urllib
import json
import os
import geocoder
from navi_firebase import firebaseCRUD
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyrebase
from flask import Flask
from flask import request
from flask import make_response


def makeWebhookResult(req):

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

    

    if req.get("queryResult").get("action") == "navigate": 
        speech = "May I help you?"
        print("Response:")
        print(speech)
        return {
        #"fulfillmentText":speech,
        #"speech": speech, only available to V1
        #"displayText": speech, 
        #"data": {},
        #"contextOut": [],
            #"source": "FinancialAidChatBot",
            "fulfillmentMessages":[
                {
                    "platform": "FACEBOOK",
                    "quickReplies":{
                        "title": speech,
                        "quickReplies":
                           [
                                #"current location",
                                "give me a direction",
                                #"history location"  
                           ]
                       
                        }
                    
                    }
                ]
    }
    elif req.get("queryResult").get("action") == "subCurrent":
        sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id") 
        #userlocation = req.get("originalDetectIntentRequest").get("payload").get("data").get("coordinates").get("lat")
        #userlocation = req.get("originalDetectIntentRequest").get("payload").get("data").get("coordinates").get("long")
        speech = "you need to send ur current location to me 1st"
        print("Response:")
        print(speech)
        return {
            #"fulfillmentText": sender
            }

    elif req.get("queryResult").get("action") == "navigation":
        sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
        origins = req.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
       # speech = " Please tell me your current building and what building you want to go"
        speech = "where are you?"

        print("Response:")
        print(speech)
        return{
              "fulfillmentText": speech          
              }

    elif req.get("queryResult").get("action") == "show_image":

        output = req.get("queryResult").get("outputContexts")
        origins = ""
        destination = ""
        name = ""
        for context in output:
             if 'location_origins' in context.get('parameters'):
                 origins = context.get('parameters').get('location_origins')
             if 'location_destination' in context.get('parameters'):
                 destination = context.get('parameters').get('location_destination')
        name = str(origins)+"-to-"+str(destination)
       
        ref = db.reference('navigation/building')
        description = ref.get()
        token = ""
        for key, val in description.items():
          if key == name:
             for key,val in val.items():
                if key == "imgToken":
                  token = val
        #print(name)
        #print(token)
        fileName = str(destination)+".jpg"
        #getUrl =  storage.child("images/"+ "TanSiewSin").get_url(token)
        getUrl =  storage.child("images/"+fileName).get_url(token)
        #print(getUrl) 
        #speech = "Please tell me your current building and what building you want to go"
        speech = fileName
        print("Response:")
        
        print(speech)
        return{
               "fulfillmentMessages":[
                {
                    "platform": "FACEBOOK",
                    "image": {
                        
                        "imageUri": getUrl
                        }
                    }
                ]      
              }

    elif req.get("queryResult").get("action") == "location_Citic":
       # sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
       # current_location = req.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
        destination = ""
        origins = ""
        destination = req.get("queryResult").get("parameters").get("location_destination")
        origins = req.get("queryResult").get("parameters").get("location_origins")
        
        
        
        speech = "where you want to go?"
        print("Response:")
        print(speech)
        #output = req.get("queryResult").get("outputContexts").get("location_origins")
        return{ 
            "fulfillmentText": speech
            }     
 
    elif req.get("queryResult").get("action") == "navigate_destination":
       
        
        speech = " ok"
       
        destination = req.get("queryResult").get("parameters").get("location_destination")
        
        output = req.get("queryResult").get("outputContexts")
        origins = ""
        for context in output:
             if 'location_origins' in context.get('parameters'):
                 origins = context.get('parameters').get('location_origins')
          
        #origins = req.get("queryResult").get("outputContexts").get("parameters").get("location_origins")
        
        sup = str(origins)+"-to-"+str(destination)
        print(sup)
        #get data from firebase  
        ref = db.reference('navigation/building')
        description = ref.get()
        descrip = ""
        print(description)
        for key, val in description.items():
          if key == sup:
             for key,val in val.items():
                if key == "description":
                  descrip = val

        print("Response:")
        print(speech)
        return{
            "fulfillmentMessages":[
                {
                    "platform": "FACEBOOK",
                    "quickReplies":{    
                        "title": descrip,
                        "quickReplies":
                           [
                                "show image"
                           ]   
                        }
                    }
                ]
            }

    elif req.get("queryResult").get("action") == "history":
        return{
              "fulfillmentText": "Hi" #ref.get()           
              }
 
          


