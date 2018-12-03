from fbbotw import fbbotw
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from fa_firebase import firebaseCRUD
from datetime import datetime as dt
import datetime
import navigation

app = Flask(__name__)

subOpt = False
fileExist = False

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
    global subOpt
    global fileExist
    subOpt = False
    fileExist = False
    
    if req.get("queryResult").get("action") == "sub":
        msg = subscribe(req)

    elif req.get("queryResult").get("action") == "subType":
        msg = subscribeType(req)

    elif req.get("queryResult").get("action") == "unsub":
        msg = unsubscribe(req)

    elif req.get("queryResult").get("action") == "unsubType":
        msg = unsubscribeType(req)
        
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
    elif req.get("queryResult").get("action") == "subscribeQuickReply":
        msg = subQuickReply(req)
    elif req.get("queryResult").get("action") == "sendFile":
        fileUrl = sendFile(req)
        return {
            "fulfillmentMessages":[{
                "payload":{
                    "facebook":{
                        "attachment":{
                            "type":"file",
                            "payload":{
                                "url": fileUrl
                                }
                            }
                        }
                    }
                }]
            }

    if subOpt == True and fileExist == True:
        return {
            "fulfillmentMessages":[
                {
                    "platform": "FACEBOOK",
                    "quickReplies":{
                        "title": msg,
                        "quickReplies":[
                            "Subscribe now",
                            "Get Pdf file"  
                            ]
                       
                        }
                    
                    }
                ]
            }
    elif subOpt == True:
        return {
            "fulfillmentMessages":[
                {
                    "platform": "FACEBOOK",
                    "quickReplies":{
                        "title": msg,
                        "quickReplies":[
                            "Subscribe now",  
                            ]
                        }
                    }
                ]
            }
    elif fileExist == True:
        return {
            "fulfillmentMessages":[
                {
                    "platform": "FACEBOOK",
                    "quickReplies":{
                        "title": msg,
                        "quickReplies":[
                            "Get Pdf file"  
                            ]             
                        }
                    }
                ]
            }
    if not msg:
        return navigation.makeWebhookResult(req)
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
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    subscribed = False
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            msg = "The amount you can get are "
            msg += y.get('offerAmt')
            sub = firebase.retrieveSub(x)
            for a,b in sub.items():
                if b.get('fbId') == sender:
                    subscribed = True
            if subscribed == False:
                msg += "\n\nFor more information, you can subscribe to "+y.get('name')+" to receive updates."
                global subOpt
                subOpt = True
            if y.get('website') != "None":
                msg += "\n\nYou may also get more information about "+ y.get('name')+ " by visiting "+y.get('website')+'.'
        if y.get('pdfToken')!= 'None':
            msg += "\n\n Or you may get more information by requesting the pdf file."
            global fileExist
            fileExist = True
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def getPeriod(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    subscribed = False
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            msg = "The application period of " + y.get('name') +' is '
            msg += 'from ' + y.get('startDate') + ' to ' + y.get('endDate')
            sub = firebase.retrieveSub(x)
            for a,b in sub.items():
                if b.get('fbId') == sender:
                    subscribed = True
            if subscribed == False:
                global subOpt
                subOpt = True
                msg += "\n\nFor more information, you can subscribe to "+y.get('name')+" to receive updates."
            if y.get('website') != "None":
                msg += "\n\nYou may also get more information about "+ y.get('name')+ " by visiting "+y.get('website')+'.'
        if y.get('pdfToken')!= 'None':
            msg += "\n\n Or you may get more information by requesting the pdf file."
            global fileExist
            fileExist = True
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def getCriteria(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    subscribed = False
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            faId = x
            criteria = firebase.retrieveCritList(faId)
            msg = "The criteria of applying " + y.get('name') +' are:'
            for c in criteria:
                msg += '\n\u2022 ' + c
            sub = firebase.retrieveSub(x)
            for a,b in sub.items():
                if b.get('fbId') == sender:
                    subscribed = True
            if subscribed == False:
                global subOpt
                subOpt = True
                msg += "\n\nFor more information, you can subscribe to "+y.get('name')+" to receive updates."
            if y.get('website') != "None":
                msg += "\n\nYou may also get more information about "+ y.get('name')+ " by visiting "+y.get('website')+'.'
            break
        if y.get('pdfToken')!= 'None':
            msg += "\n\n Or you may get more information by requesting the pdf file."
            global fileExist
            fileExist = True
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def getDocument(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    subscribed = False
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            faId = x
            document = firebase.retrieveDocList(faId)
            msg = "The documents required to apply " + y.get('name') +' are:'
            for d in document:
                msg += '\n\u2022 ' + d
            sub = firebase.retrieveSub(x)
            for a,b in sub.items():
                if b.get('fbId') == sender:
                    subscribed = True
            if subscribed == False:
                global subOpt
                subOpt = True
                msg += "\n\nFor more information, you can subscribe to "+y.get('name')+" to receive updates."
            if y.get('website') != "None":
                msg += "\n\nYou may also get more information about "+ y.get('name')+ " by visiting "+y.get('website')+'.'
            break
        if y.get('pdfToken')!= 'None':
            msg += "\n\n Or you may get more information by requesting the pdf file."
            global fileExist
            fileExist = True
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def getProcedure(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    msg = ""
    subscribed = False
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            faId = x
            procedure = firebase.retrieveProList(faId)
            msg = "The procedure to apply " + y.get('name') +' are:'
            for p in procedure:
                msg += '\n\u2022 ' + p
            sub = firebase.retrieveSub(x)
            for a,b in sub.items():
                if b.get('fbId') == sender:
                    subscribed = True
            if subscribed == False:
                global subOpt
                subOpt = True
                msg += "\n\nFor more information, you can subscribe to "+y.get('name')+" to receive updates."
            if y.get('website') != "None":
                msg += "\n\nYou may also get more information about "+ y.get('name')+ " by visiting "+y.get('website')+'.'
            break
        if y.get('pdfToken')!= 'None':
            msg += "\n\n Or you may get more information by requesting the pdf file."
            global fileExist
            fileExist = True
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def subscribe(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    msg = ""
            
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            subscription = {
                    "id": x,
                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                    #"status": 'active',
                    "fbId": sender
                }
            subList = firebase.retrieveSub(x)
            for s,t in subList.items():
                if t.get('fbId') == sender:
##                    if t.get('status') == 'inactive':
##                        firebase.updateSub(subscription,s)
##                        msg = "You resubscribed to " + y.get('name') +'.'
##                    else:
                    msg = "You already subscribed to " + y.get('name')+'.'
                    return msg
            msg = "You are now subscribed to " + y.get('name')+'.'
            
            firebase.addSub(subscription)
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def subscribeType(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    if not name:
        if fa:
            msg = 'List of financial aid you can subscribe. Type "Subscribe" followed by the financial aid name to subscribe'
            for x,y in fa.items():
                msg +=  '\n\u2022 ' + y.get('name')
        else:
            msg = "There is no financial aid right now."
    elif name == 'study loan':
        if fa:
            msg = 'List of study loan you can subscribe. Type "Subscribe" followed by the study loan name to subscribe'
            for x,y in fa.items():
                if y.get('type') == 'Study Loan': 
                    msg +=  '\n\u2022 ' + y.get('name')
        else:
            msg = "There is no study loan right now."
    elif name == 'scholarship':
        if fa:
            msg = 'List of scholarship you can subscribe. Type "Subscribe" followed by the scholarship name to subscribe'
            for x,y in fa.items():
                if y.get('type') == 'Scholarship': 
                    msg +=  '\n\u2022 ' + y.get('name')
        else:
            msg = "There is no scholarship right now."
    elif name == 'PTPTN':
        if fa:
            msg = 'List of PTPTN you can subscribe. Type "Subscribe" followed by the PTPTN name to subscribe'
            for x,y in fa.items():
                if y.get('type') == 'PTPTN':
                    msg +=  '\n\u2022 ' + y.get('name')
        else:
            msg = "There is no PTPTN right now."
    return msg

def unsubscribe(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    msg = ""
    subscribed = False        
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            subList = firebase.retrieveSub(x)
            for s,t in subList.items():
                if t.get('fbId') == sender:
                    subscribed = True
                    firebase.deleteSub(s,x)
                    msg = "You unsubscribed to " + y.get('name')+'.'
                    break
            if subscribed == False:
                msg = "You did not subscribed to " + y.get('name')
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def unsubscribeType(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    name = req.get("queryResult").get("parameters").get("financialAid")
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    subscribed = False
    msg = ''
    if not name:
        if fa:
            msg = 'List of financial aid you subscribed. Type "Unsubscribe" followed by the financial aid name to unsubscribe'
            for x,y in fa.items():
                sub = firebase.retrieveSub(x)
                for s,t in sub.items():
                    if t.get('fbId') == sender:
                        subscribed = True
                        msg +=  '\n\u2022 ' + y.get('name')
                        break
            if subscribed == False:
                msg = "You did not subscribe any financial aid."
        else:
            msg = "There is no financial aid right now."
    elif name == 'study loan':
        if fa:
            msg = 'List of study loan you subscribed. Type "Unsubscribe" followed by the study loan name to unsubscribe'
            for x,y in fa.items():
                if y.get('type') == 'Study Loan':
                    sub = firebase.retrieveSub(x)
                    for s,t in sub.items():
                        if t.get('fbId') == sender:
                            subscribed = True
                            msg +=  '\n\u2022 ' + y.get('name')
                            break
            if subscribed == False:
                msg = "You did not subscribe any study loan."
        else:
            msg = "There is no study loan right now."
    elif name == 'scholarship':
        if fa:
            msg = 'List of scholarship you subscribed. Type "Unsubscribe" followed by the scholarship name to unsubscribe'
            for x,y in fa.items():
                if y.get('type') == 'Scholarship': 
                    sub = firebase.retrieveSub(x)
                    for s,t in sub.items():
                        if t.get('fbId') == sender:
                            subscribed = True
                            msg +=  '\n\u2022 ' + y.get('name')
                            break
            if subscribed == False:
                msg = "You did not subscribe any scholarship."
        else:
            msg = "There is no scholarship right now."
    elif name == 'PTPTN':
        if fa:
            msg = 'List of PTPTN you subscribed. Type "Unsubscribe" followed by the PTPTN name to unsubscribe'
            for x,y in fa.items():
                if y.get('type') == 'PTPTN':
                    sub = firebase.retrieveSub(x)
                    for s,t in sub.items():
                        if t.get('fbId') == sender:
                            subscribed = True
                            msg +=  '\n\u2022 ' + y.get('name')
                            break
            if subscribed == False:
                msg = "You did not subscribe any PTPTN."
        else:
            msg = "There is no PTPTN right now."
    return msg

def subQuickReply(req):
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    output = req.get("queryResult").get("outputContexts")
    for context in output:
        if 'financialAid' in  context.get('parameters'):
            name = context.get('parameters').get('financialAid')
            break
    sender = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    msg = ""
            
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            subscription = {
                    "id": x,
                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                    #"status": 'active',
                    "fbId": sender
                }
            subList = firebase.retrieveSub(x)
            for s,t in subList.items():
                if t.get('fbId') == sender:
##                    if t.get('status') == 'inactive':
##                        firebase.updateSub(subscription,s)
##                        msg = "You resubscribed to " + y.get('name') +'.'
##                    else:
                    msg = "You already subscribed to " + y.get('name')+'.'
                    return msg
            msg = "You are now subscribed to " + y.get('name')+'.'
            
            firebase.addSub(subscription)
    if not msg:
        msg = "I do not find any financial aid called " + name
    return msg

def sendFile(req):
    token = ""
    filename = ""
    firebase = firebaseCRUD()
    output = req.get("queryResult").get("outputContexts")
    for context in output:
        if 'financialAid' in  context.get('parameters'):
            name = context.get('parameters').get('financialAid')
            break
    fa = firebase.retrieveFAWithKey()
    for x,y in fa.items():
        if y.get('name').lower() == name.lower():
            token = y.get('pdfToken')
            filename = y.get('name')+'.pdf'
    fileUrl = firebase.getFaUrl(filename,token)
    return fileUrl

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
