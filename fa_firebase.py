import pyrebase
import re
import datetime
class firebaseCRUD:
    
    config = {
      "apiKey": "AIzaSyBJYcE3HXN7CZaV9qBflNJwMgt6q2vQJ1g",
      "authDomain": "joe-mlidnd.firebaseapp.com",
      "databaseURL": "https://joe-mlidnd.firebaseio.com",
      "storageBucket": "joe-mlidnd.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)

    auth = firebase.auth()

    user = auth.sign_in_with_email_and_password("chanjy501@gmail.com", "123456")

    db = firebase.database()


    def retrieveFA(self):
        fa = []
        fas = self.db.child("Financial_aid").get()
        if fas.val():
            for x in fas.each():
                    #if x.key() == faId:
                fa.append(x.val())
        return fa

    def retrieveFAWithKey(self):
        fa = {}
        fas = self.db.child("Financial_aid").get()
        if fas.val():
            for x in fas.each():
                fa[x.key()] = x.val()
                #if x.key() == faId:
                #fa.append(x.val())
        return fa


    #return list of criteria name
    def retrieveCritList(self,faId):
        criterion = []
        criteria = self.db.child("Criteria").get()
        #print(criterion.val())
        for x in criteria.each():
            if x.key() == faId:
                print(x.val().values())
                for item in x.val().values():
                    for value in list(item.values()):
                        criterion.append(value)
                    #for value in item.val():
                   # criteria[CId] = c
        #print(criteria)
        return criterion


    #return list of document name
    def retrieveDocList(self,faId):
        doc = []
        docs = self.db.child("Documents").get()
        #print(criterion.val())
        for x in docs.each():
            if x.key() == faId:
                print(x.val().values())
                for item in x.val().values():
                    for value in list(item.values()):
                        doc.append(value)
                    #for value in item.val():
                   # criteria[CId] = c
        #print(criteria)
        return doc


    #return list of document name
    def retrieveProList(self,faId):
        procedure = []
        procedures = self.db.child("Procedures").get()
        #print(criterion.val())
        for x in procedures.each():
            if x.key() == faId:
                print(x.val().values())
                for item in x.val().values():
                    for value in list(item.values()):
                        procedure.append(value)
                    #for value in item.val():
                   # criteria[CId] = c
        #print(criteria)
        return procedure

    def addSub(self,subscription):
        subId = retrieveNextSubId(self)
        self.db.child("Subscription").child(subId).set(subscription)
        
    def retrieveNextSubId(self):
        lastId = ""
        subIds = self.db.child("Subscription").shallow().get()
        
        if subIds.val():
            for x in subIds.val():
                if not lastId:
                    lastId = x
                elif lastId < x:
                    lastId = x
            splitId = re.split('(\d+)',lastId)
            lastId = int(splitId[1]) + 1
            lastId = 'S' + "{0:0=4d}".format(lastId)
            
        else:
            lastId = "S0001"
        return lastId


