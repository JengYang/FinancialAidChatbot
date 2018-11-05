
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

@app.route('/')
def index():
    return '<h1>App deployed</h1>'

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
        msg = subscribe(req)
        
    elif req.get("queryResult").get("action") == "getAvailable":
        msg = availableFA(req)       
        
    elif req.get("queryResult").get("action") == "amount":
        msg = getAmt(req)
            
    elif req.get("queryResult").get("action") == "applicationPeriod":
        msg = getPeriod(req)
    elif req.get("queryResult").get("action") == "criteria":
        msg = getCriteria(req)
    elif req.get("queryResult").get("action") == "document":
        msg = getDocument(req)
    elif req.get("queryResult").get("action") == "procedure":
        msg = getProcedure(req)
    elif req.get("queryResult").get("action") == "AllFA":
        msg = allFA(req)
    return {
        "fulfillmentText":msg
        }

def allFA(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFA()
    name = []
    if req.get("queryResult").get("parameters").get("financialAid").lower() == 'financial aid':
        for x in fa:
            name.append(x.get('name'))
        if name:
            msg = "List of financial aids that you may apply:"
            for n in name:
                msg += '\n\u2022 ' + n
        else:
            msg = "There is no financial aid right now."
        
            
    elif req.get("queryResult").get("parameters").get("financialAid") == 'scholarship':
        for x in fa:
            if x.get('type') == 'Scholarship':
                name.append(x.get('name'))
        if name:
            msg = 'List of scholarships that you may apply:'
            for n in name:
                msg += '\n\u2022 ' + n
        else:
            msg = "There is no scholarship right now."
    elif req.get("queryResult").get("parameters").get("financialAid") == 'study loan':       
        for x in fa:
            if x.get('type') == 'Study Loan':
                name.append(x.get('name'))
        if name:
            msg = 'List of study loans that you may apply:'
            for n in name:
                msg += '\n\u2022 ' + n
        else:
            msg = "There is no study loan right now"
    elif req.get("queryResult").get("parameters").get("financialAid") == 'PTPTN':       
        for x in fa:
            if x.get('type') == 'PTPTN':
                name.append(x.get('name'))
        if name:
            msg = 'List of PTPTN : '
            for n in name:
                msg += '\n\u2022 ' + n
        else:
            msg = "There is no PTPTN."
    else:
        msg = "I do not get what you say, please try again."

    return msg

def availableFA(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFA()
    name = []
    present = datetime.date.today()
    if req.get("queryResult").get("parameters").get("financialAid").lower() == 'financial aid':
        for x in fa:
            start = dt.strptime(x.get('startDate'),"%Y-%m-%d").date()
            end = dt.strptime(x.get('endDate'),"%Y-%m-%d").date()
            if present >= start and present <= end:
                name.append(x.get('name'))
        if name:
            msg = 'The available financial aids are : '
            for n in name:
                msg += '\n\u2022 ' + n
        else:
            msg = "There is no financial aid available right now."
        
            
    elif req.get("queryResult").get("parameters").get("financialAid") == 'scholarship':
        for x in fa:
            start = dt.strptime(x.get('startDate'),"%Y-%m-%d").date()
            end = dt.strptime(x.get('endDate'),"%Y-%m-%d").date()
            if present >= start and present <= end:
                if x.get('type') == 'Scholarship':
                    name.append(x.get('name'))
        if name:
            msg = 'The available scholarships are : '
            for n in name:
                msg += '\n\u2022 ' + n
        else:
            msg = "There is no scholarship available right now."
    elif req.get("queryResult").get("parameters").get("financialAid") == 'study loan':       
        for x in fa:
            start = dt.strptime(x.get('startDate'),"%Y-%m-%d").date()
            end = dt.strptime(x.get('endDate'),"%Y-%m-%d").date()
            if present >= start and present <= end:
                if x.get('type') == 'Study Loan':
                    name.append(x.get('name'))
        if name:
            msg = 'The available study loans are : '
            for n in name:
                msg += '\n\u2022 ' + n
        else:
            msg = "There is no study loan available right now"
    elif req.get("queryResult").get("parameters").get("financialAid") == 'PTPTN':       
        for x in fa:
            start = dt.strptime(x.get('startDate'),"%Y-%m-%d").date()
            end = dt.strptime(x.get('endDate'),"%Y-%m-%d").date()
            if present >= start and present <= end:
                if x.get('type') == 'PTPTN':
                    name.append(x.get('name'))
        if name:
            msg = 'The available PTPTN are : '
            for n in name:
                msg += '\n\u2022 ' + n
        else:
            msg = "PTPTN is not available right now"
    else:
        msg = "I do not get what you say, please try again."
    return msg

def getAmt(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFA()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    for x in fa:
        if x.get('name').lower() == name.lower():
            msg = "The amount you can get are "
            msg += x.get('offerAmt')
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def getPeriod(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFA()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    for x in fa:
        if x.get('name').lower() == name.lower():
            msg = "The application period of " + x.get('name') +' is '
            msg += 'from ' + x.get('startDate') + ' to ' + x.get('endDate')
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def getCriteria(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            faId = x
            criteria = firebase.retrieveCritList(faId)
            msg = "The criteria of applying " + y.get('name') +' are:'
            for c in criteria:
                msg += '\n\u2022 ' + c
            break
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def getDocument(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            faId = x
            document = firebase.retrieveDocList(faId)
            msg = "The documents required to apply " + y.get('name') +' are:'
            for d in document:
                msg += '\n\u2022 ' + d
            break
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def getProcedure(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            faId = x
            procedure = firebase.retrieveProList(faId)
            msg = "The procedure to apply " + y.get('name') +' are:'
            for p in procedure:
                msg += '\n\u2022 ' + p
            break
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def subscribe(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    msg = ""
    #testing
    if not name:
        if fa:
            msg = "Which financial aid u want to subscribe?\n"
            for x,y in fa.items():
                msg +=  '\n\u2022 ' + y.get('name')
        else:
            msg = "There is no financial aid right now."
    #end testing
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            subList = firebase.retrieveSub(x)
            for s in subList:
                if s.get('fbId') == sender:
                    msg = "You already subscribed to " + y.get('name')+'.'
                    return msg
            msg = "You are now subscribed to " + y.get('name')+'.'
            subscription = {
                    "id": x,
                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                    "status": 'active',
                    "fbId": sender
                }
            firebase.addSub(subscription)
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg
        

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
