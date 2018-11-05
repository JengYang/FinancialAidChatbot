from fbbotw import fbbotw
from fa_firebase import firebaseCRUD
#add new code for subscription in future
#...

#test for sending message
def sendMsg():
    firebase = firebaseCRUD()
    fa = firebase.retrieveFAWithKey()
    for a in fa:
        print(a)
    #fbbotw.post_text_message('2160418613974674',"Hi,XD",'RESPONSE',None) 
