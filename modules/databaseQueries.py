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
                        Field("userId","integer"), Field("givenAnswer","string"),
                        Field('timeOfSubmission','datetime',writable = False)
                    )
    
    db.define_table("authorPassageMapping",
                        Field("id","integer"), Field("passageId","integer"),
                        Field("userId","integer"),Field('timeOfSubmission','datetime',writable = False))

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
This function updates a passage's contents.
"""
def updatePassage(db, passageId, newContent):
    row = db(db.passages.id==passageId).select().first()
    row.content = newContent
    row.update_record()

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
    
"""
Given a passageId, the average score is returned.
"""
def getAverageScore(db, passageId):
    rows = db(db.passageStats.passageId == passageId).select()
    count = len(rows)
    if(count == 0):
        count = 1
    total = 0
    for row in rows:
        total += row.score
    average = float(total)/float(count)
    return average
 
"""
Given a passageId, the average time taken is returned.
"""
def getAverageTime(db, passageId):
    rows = db(db.passageStats.passageId == passageId).select()
    count = len(rows)
    if(count == 0):
        count = 1
    total = 0
    for row in rows:
        total += row.timeTaken
    average = float(total)/float(count)
    return average

"""
Given a passageId, the number of attempts at solving this passage is returned.
"""
def getNumberOfAttempts(db, passageId):
    rows = db(db.passageStats.passageId == passageId).select()
    count = len(rows)
    return count

"""
Given a questionId, the answer distribution is returned.
"""
def getAnswerDistribution(db, questionId):
    rows = db(db.submittedAnswers.questionId == questionId).select()
    aCount = 0
    bCount = 0
    cCount = 0
    dCount = 0
    eCount = 0
    noneCount = 0
    for row in rows:
        if(row.givenAnswer=="A"):
            aCount += 1
        if(row.givenAnswer=="B"):
            bCount += 1
        if(row.givenAnswer=="C"):
            cCount += 1
        if(row.givenAnswer=="D"):
            dCount += 1
        if(row.givenAnswer=="E"):
            eCount += 1
        else:
            noneCount += 1

    answerDict = {}
    answerDict["A"] = aCount
    answerDict["B"] = bCount
    answerDict["C"] = cCount
    answerDict["D"] = dCount
    answerDict["E"] = eCount
    answerDict["N/A"] = noneCount
    return answerDict

"""
Given a passageId, the answer distributions of each of its questions are returned.
"""
def getPassageQuestionAnswerDistribution(db, passageId):
    answerDicts = []
    rows = getQuestions(db, passageId)
    for row in rows:
        questionId = row.id
        answerDicts.append(getAnswerDistribution(db, questionId))
    return answerDicts
    
"""
This function inserts a user passage mapping when that user adds a passage.
"""
def insertUserPassageMapping(db, userId, passageId):
    db.authorPassageMapping.insert(passageId = passageId, userId = userId)

"""
Given a userId, the list of passages submitted by a user is returned.
"""
def getUserSubmittedPassages(db, userId):
    rows = db(db.authorPassageMapping.userId == userId).select()
    passageIds = []
    for row in rows:
        passageIds.append(int(row.passageId))
    return passageIds

"""
This function will return the number of registered users
"""
def getNumberOfUsers(db): 
    rows = db(db.auth_user.id != 0).select()
    return len(rows)

"""
Gets a user distribution based on countries.
"""
def getUserDistribution(db):
    count = db.auth_user.id.count()
    result = db().select(db.auth_user.Location, count, groupby = db.auth_user.Location)
    return result

"""
The number of passage instances solved after a given time.
"""
def getNumberOfPassageInstancesSolved(db, time):
    rows = db(db.passageStats.timeOfSubmission >= time).select()
    count = len(rows)
    return count