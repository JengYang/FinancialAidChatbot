import pyrebase
import re
import datetime
from datetime import datetime as dt
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

    def retrieveFaIDs(self):
        faIds = self.db.child("Financial_aid").shallow().get()
        return sorted(list(faIds.val()))

    def retrieveNextFaID(self):
        lastId = ""
        faIds = self.db.child("Financial_aid").shallow().get()
        
        if faIds.val():
            for x in faIds.val():
                if not lastId:
                    lastId = x
                elif lastId < x:
                    lastId = x
            splitId = re.split('(\d+)',lastId)
            lastId = int(splitId[1]) + 1
            lastId = 'F' + "{0:0=4d}".format(lastId)
            
        else:
            lastId = "F0001"
        return lastId

    def retrieveDocId(self):
        lastDocId =""
        documents = self.db.child("Documents").get()
        print(documents.val())
        if documents.val():
            for x in documents.each():
                print(x.val().keys())
                for key in x.val().keys():
                    print(key)
                    if not lastDocId:
                        lastDocId = key
                    elif lastDocId < key:
                        lastDocId = key
        else:
            lastDocId = "D0000"
        return lastDocId

    def retrieveCriId(self):
        lastCriId =""
        criteria = self.db.child("Criteria").get()
        print(criteria.val())
        if criteria.val():
            for x in criteria.each():
                print(x.val().keys())
                for key in x.val().keys():
                    print(key)
                    if not lastCriId:
                        lastCriId = key
                    elif lastCriId < key:
                        lastCriId = key
        else:
            lastCriId = "C0000"
        return lastCriId

    def retrieveProId(self):
        lastProId =""
        procedures = self.db.child("Procedures").get()
        print(procedures.val())
        if procedures.val():
            for x in procedures.each():
                print(x.val().keys())
                for key in x.val().keys():
                    print(key)
                    if not lastProId:
                        lastProId = key
                    elif lastProId < key:
                        lastProId = key
        else:
            lastProId = "P0000"

        return lastProId


    def retrieveFA(self):
        fa = []
        fas = self.db.child("Financial_aid").get()
        if fas.val():
            for x in fas.each():
                #if x.key() == faId:
                fa.append(x.val())
        return fa

    #return the whole criteria object (include criteria id)
    def retrieveCriteria(self,faId):
        criterion = {}
        criteria = self.db.child("Criteria").get()
        #print(criterion.val())
        for x in criteria.each():
            if x.key() == faId:
                for cId in x.val().keys():
                    c = {}
                    for item in x.val().values():
                        c = item
                    criterion[cId] = c
        return criterion

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

    #return the whole documents object (include document id)
    def retrieveDoc(self,faId):
        doc = {}
        docs = self.db.child("Documents").get()
        #print(criterion.val())
        for x in docs.each():
            if x.key() == faId:
                for dId in x.val().keys():
                    d = {}
                    for item in x.val().values():
                        d = item
                    doc[dId] = d
        return doc

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

    #return the whole procedure object (include procedure id)
    def retrievePro(self,faId):
        procedure = {}
        procedures = self.db.child("Procedures").get()
        #print(criterion.val())
        for x in procedures.each():
            if x.key() == faId:
                for pId in x.val().keys():
                    d = {}
                    for item in x.val().values():
                        d = item
                    procedure[pId] = d
        return procedure

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

