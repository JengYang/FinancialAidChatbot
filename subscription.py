from fbbotw import fbbotw
from fa_firebase import firebaseCRUD
import datetime
#add new code for subscription in future
#...

#test for sending message
def sendMsg():
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    present = datetime.date.today()
    for a,b in fa.items():
        
        if datetime.datetime.strptime(b.get('startDate'),"%Y-%m-%d").date() == present:
            sub = firebase.retrieveSub(a)
            print(sub)
            for s in sub:
                #if s.get('status') == 'active': #if status is needed
                msg = b.get('name')+" application starts today. Apply now."
                fbbotw.post_text_message(s.get('fbId'),msg,'RESPONSE',None) 
        elif datetime.datetime.strptime(b.get('endDate'),"%Y-%m-%d").date() == present:
            sub = firebase.retrieveSub(a)
            for s in sub:
                msg = b.get('name')+" application ends today. Apply now." 
                fbbotw.post_text_message(s.get('fbId'),msg,'RESPONSE',None)      
    #fbbotw.post_text_message('2160418613974674',"Hi,XD",'RESPONSE',None) 


sendMsg()
