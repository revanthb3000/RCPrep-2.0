#Dead code to get intellisense to 
if 0:
    from modules import *
    from gluon import *
    request, session, response, T, cache = current.request, current.session, current.response, current.t, current.cache
    from gluon.tools import Auth, Service, Crud
    db = DAL('mysql://username:password@localhost/test')
    auth = Auth()
    service = Service()
    crud = Crud()

import databaseConnectionStrings
import utilityFunctions
import datetime

def index(): 
    redirect(URL('passages','solvePassage'))
    return dict()

def solvePassage():
    response.view = 'passages/solvePassage.html'
    response.title = "Solve A Passage"
    response.ignoreHeading = True
    
    passageId = request.vars.passageId
    if(not(utilityFunctions.checkIfVariableIsInt(passageId))):
        numberOfPassages = databaseQueries.getNumberOfPassages(db)
        passageId = utilityFunctions.getRandomNumber(1, numberOfPassages)

    passageContent = databaseQueries.getPassage(db, passageId)
    questionContent = utilityFunctions.getQuestionsHTMLCode(db, passageId)
    numberOfQuestions = databaseQueries.getNumberOfQuestions(db, passageId)
    fields = []
    fields += [Field("startTime", 'datetime')]
    fields += [Field("passageId", 'string')]
    for i in range(1, numberOfQuestions + 1):
        questionNumber = "question-" + str(i)
        fields += [Field(questionNumber,'string')]

    form = SQLFORM.factory(*fields, _action = URL('passages','passageResults'))

    startTime = datetime.datetime.now()
    return dict(form = form, passageId = passageId, startTime = startTime, passageContent = passageContent, questionContent = questionContent)

def passageResults():
    response.view = 'passages/passageResults.html'
    response.title = "Results"
    
    passageId = request.vars.passageId
    if(not(utilityFunctions.checkIfVariableIsInt(passageId))):
        redirect(URL('passages','solvePassage'))

    startTime = datetime.datetime.strptime(str(request.vars.startTime),'%Y-%m-%d %H:%M:%S.%f')
    curTime = datetime.datetime.now()
    elapsedTime = curTime - startTime
    elapsedTimeStr = str(elapsedTime)
    elapsedTimeStr = str(elapsedTimeStr.split(":")[1]) + ":" + str(elapsedTimeStr.split(":")[2].split(".")[0])
    
    numberOfQuestions = databaseQueries.getNumberOfQuestions(db, passageId)
    answers = []
    for i in range(1, numberOfQuestions + 1):
        questionId = "question-" + str(i)
        answers += [request.vars[questionId]]

    passageContent = databaseQueries.getPassage(db, passageId)
    questionContent = utilityFunctions.getResultsReviewHTMLCode(db, passageId, answers)
    resultsContent = utilityFunctions.getResultsHTMLCode(db, passageId, answers)

    return dict(passageContent = passageContent, questionContent = questionContent, resultsContent = resultsContent, elapsedTime = elapsedTimeStr)