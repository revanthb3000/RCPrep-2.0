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
    
    db.define_table("passageStats",
                        Field("id","integer"), Field("passageId","integer"),
                        Field("userId","integer"), Field("timeTaken","integer"), #Time Taken is in seconds
                        Field("score","integer"), Field('timeOfSubmission','datetime',writable = False)
                    )
    
    db.define_table("submittedAnswers",
                        Field("id","integer"), Field("questionId","integer"),
                        Field("userId","integer"), Field("givenAnswer","string"), #Time Taken is in seconds
                        Field('timeOfSubmission','datetime',writable = False)
                    )

"""
Given a passageId, this function returns the content of the passage.
"""
def getPassage(db, passageId):
    rows = db(db.passages.id == passageId).select()
    content = ""
    if(len(rows)==1):
        content = rows[0].content
    return content

"""
Adds a passage to the DB and returns the passageId
"""
def addPassage(db, passageContent):
    passageId = db.passages.insert(content = passageContent)
    return passageId

"""
Adds a question to the DB and returns the questionId
"""
def addQuestion(db, passageId, question, optionA, optionB, optionC, optionD, optionE, answer):
    db.questions.insert(passageId = passageId, question = question, optionA = optionA, optionB = optionB, 
                        optionC = optionC, optionD = optionD, optionE = optionE, answer = answer)

"""
Given a passageId, the questions related to that passage are returned.
"""
def getQuestions(db, passageId):
    rows = db(db.questions.passageId == passageId).select()
    return rows

"""
Returns the total number of passages present in the database.
"""
def getNumberOfPassages(db):
    rows = db(db.passages.id != 0).select()
    return len(rows)

"""
Given a passageId, the number of questions tagged under that passage.
"""
def getNumberOfQuestions(db, passageId):
    rows = db(db.questions.passageId == passageId).select()
    return len(rows)

"""
This function is used to insert entries into the passage Stats table.
"""
def insertPassageStats(db, passageId, userId, timeTaken, score):
    db.passageStats.insert(passageId = passageId, userId = userId, timeTaken = timeTaken, score = score)
    
"""
This function is used to insert entries into the submittedAnswers table.
"""
def insertAnswerStats(db, questionId, userId, givenAnswer):
    db.submittedAnswers.insert(questionId = questionId, userId = userId, givenAnswer = givenAnswer)