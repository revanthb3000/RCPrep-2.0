from gluon import *

"""
Define all your tables over here. This function is called in db.py
"""
def defineDBTables(db, userId):
    if(userId==None):
        userId = 0

    #Add all define_table statements in here.
    db.define_table("passages",
                        Field("id","integer"), Field("content","text")
                    )
    
    db.define_table("questions",
                        Field("id","integer"), Field("passageId","integer"), 
                        Field("question","text"), Field("optionA","text"), 
                        Field("optionB","text"), Field("optionC","text"), 
                        Field("optionD","text"), Field("optionE","text"), 
                        Field("answer","string") 
                    )
    
def getPassage(db, passageId):
    rows = db(db.passages.id == passageId).select()
    content = ""
    if(len(rows)==1):
        content = rows[0].content
    return content

def getQuestions(db, passageId):
    rows = db(db.questions.passageId == passageId).select()
    return rows

def getNumberOfPassages(db):
    rows = db(db.passages.id != 0).select()
    return len(rows)

def getNumberOfQuestions(db, passageId):
    rows = db(db.questions.passageId == passageId).select()
    return len(rows)