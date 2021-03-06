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
            print(datetime.datetime.strptime(b.get('startDate'),"%Y-%m-%d").date())
            for s in sub.values():
                #if s.get('status') == 'active': #if status is needed
                msg = b.get('name')+" application starts today. Apply now."
                fbbotw.post_text_message(s.get('fbId'),msg,'RESPONSE',None) 
        elif datetime.datetime.strptime(b.get('endDate'),"%Y-%m-%d").date() == present:
            sub = firebase.retrieveSub(a)
            for s in sub.values():
                msg = b.get('name')+" application ends today. Apply now." 
                fbbotw.post_text_message(s.get('fbId'),msg,'RESPONSE',None)
        

