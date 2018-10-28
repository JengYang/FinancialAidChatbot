
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from fa_firebase import firebaseCRUD
from datetime import datetime as dt
import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    firebase = firebaseCRUD()
    if req.get("queryResult").get("action") == "financialAid": 
        #return {}
    #result = req.get("result")
   # parameters = result.get("parameters")
    #zone = parameters.get("bank-name")

    #cost = {'Andhra Bank':'6.85%', 'Allahabad Bank':'6.75%', 'Axis Bank':'6.5%', 'Bandhan bank':'7.15%', 'Bank of Maharashtra':'6.50%', 'Bank of Baroda':'6.90%', 'Bank of India':'6.60%', 'Bharatiya Mahila Bank':'7.00%', 'Canara Bank':'6.50%', 'Central Bank of India':'6.60%', 'City Union Bank':'7.10%', 'Corporation Bank':'6.75%', 'Citi Bank':'5.25%', 'DBS Bank':'6.30%', 'Dena Bank':'6.80%', 'Deutsche Bank':'6.00%', 'Dhanalakshmi Bank':'6.60%', 'DHFL Bank':'7.75%', 'Federal Bank':'6.70%', 'HDFC Bank':'5.75% to 6.75%', 'Post Office':'7.10%', 'Indian Overseas Bank':'6.75%', 'ICICI Bank':'6.25% to 6.9%', 'IDBI Bank':'6.65%', 'Indian Bank':'4.75%', 'Indusind Bank':'6.85%', 'J&K Bank':'6.75%', 'Karnataka Bank':'6.50 to 6.90%', 'Karur Vysya Bank':'6.75%', 'Kotak Mahindra Bank':'6.6%', 'Lakshmi Vilas Bank':'7.00%', 'Nainital Bank':'7.90%', 'Oriental Bank of Commerce':'6.85%', 'Punjab National Bank':'6.75%', 'Punjab and Sind Bank':'6.4% to 6.80%', 'Saraswat bank':'6.8%', 'South Indian Bank':'6% to 6.75%', 'State Bank of India':'6.75%', 'Syndicate Bank':'6.50%', 'Tamilnad Mercantile Bank Ltd':'6.90%', 'UCO bank':'6.75%', 'United Bank Of India':'6%', 'Vijaya Bank':'6.50%', 'Yes Bank':'7.10%'}
    #speech = "The interest rate of " + zone + " is " + str(cost[zone])
        speech = "Which financial aid are you looking for?"
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
                        "quickReplies":[
                            "PTPTN",
                            "Scholarship",
                            "Study loan"  
                            ]
                       
                        }
                    
                    }
                ]
    }
    elif req.get("queryResult").get("action") == "sub":
        sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
        return {
            "fulfillmentText":sender
            }
    elif req.get("queryResult").get("action") == "getAvailable":
        msg = availableFA(req)       
        return {
            "fulfillmentText":msg
            }
        
            

def availableFA(req):
    fa = firebase.retrieveFA()
    name = []
    present = datetime.date.today()
    if req.get("queryResult").get("parameters").get("financialAid").lower() == 'financial aid':
        for x in fa:
            start = dt.strptime(x.get('startDate'),"%Y-%m-%d").date()
            end = dt.strptime(x.get('endDate'),"%Y-%m-%d").date()
            if present >= start and present <= end:
                name.append(x.get('name'))
        msg = 'The available financial aids are : '
        for n in name:
            msg += '\n\u2022 ' + n
            
    elif req.get("queryResult").get("parameters").get("financialAid").lower() == 'scholarship':
        for x in fa:
            start = dt.strptime(x.get('startDate'),"%Y-%m-%d").date()
            end = dt.strptime(x.get('endDate'),"%Y-%m-%d").date()
            if present >= start and present <= end:
                if x.get('type') == 'Scholarship':
                    name.append(x.get('name'))
        msg = 'The available scholarships are : '
        for n in name:
            msg += '\n\u2022 ' + n
            
    return msg

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
