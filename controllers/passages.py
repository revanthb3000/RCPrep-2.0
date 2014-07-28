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
    userId = (auth.user.id) if (auth.is_logged_in()) else 0
    
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
    utilityFunctions.updateStats(db, passageId, userId, elapsedTime.seconds, answers)

    return dict(passageContent = passageContent, questionContent = questionContent, resultsContent = resultsContent, elapsedTime = elapsedTimeStr)

@auth.requires_login()
def submitPassage():
    response.html = "passages/submitPassage.html"
    response.title = "Submit Passage"
    firstQuestionHtmlCode = utilityFunctions.getQuestionInputHtmlCode(1)
    loadNewQuestionUrl = URL('ajax','getQuestionCode',vars=dict(questionNumber = "replaceMEQuestionNumber"))
    return dict(firstQuestionHtmlCode = firstQuestionHtmlCode, loadNewQuestionUrl = loadNewQuestionUrl)

@auth.requires_login()
def confirmPassage():
    response.html = "passages/confirmPassage.html"
    response.title = "Confirm Passage"
    passageContent = str(request.vars.passage)
    passageContent = passageContent[3:] #Gets rid of the <p> tag
    passageContent = passageContent[:-4] #Gets rid of the </p> tag
    numOfQuestions = int(request.vars.num_questions)
    questionContent = ""
    questionContent += "<input type='hidden' name='passage' value='"+passageContent+"'/>\n"
    questionContent += "<input type='hidden' name='num_questions' value='"+str(numOfQuestions)+"'/>\n"
    for i in range(1, numOfQuestions + 1):
        question = str(request.vars["question" + str(i)])
        if(question.strip()==""):
            continue
        optionA = str(request.vars["A" + str(i)])
        optionB = str(request.vars["B" + str(i)])
        optionC = str(request.vars["C" + str(i)])
        optionD = str(request.vars["D" + str(i)])
        optionE = str(request.vars["E" + str(i)])
        answer = str(request.vars["answer" + str(i)])
        questionContent += str(i) + ". " + question + "<br/>\n"
        questionContent += "<input type='hidden' name='question" + str(i) + "' value='"+question+"'/>\n"
        questionContent += "<b>(A)</b> " + optionA + "<br/>\n"
        questionContent += "<input type='hidden' name='A" + str(i) + "' value='"+optionA+"'/>\n"
        questionContent += "<b>(B)</b> " + optionB + "<br/>\n"
        questionContent += "<input type='hidden' name='B" + str(i) + "' value='"+optionB+"'/>\n"
        questionContent += "<b>(C)</b> " + optionC + "<br/>\n"
        questionContent += "<input type='hidden' name='C" + str(i) + "' value='"+optionC+"'/>\n"
        questionContent += "<b>(D)</b> " + optionD + "<br/>\n"
        questionContent += "<input type='hidden' name='D" + str(i) + "' value='"+optionD+"'/>\n"
        questionContent += "<b>(E)</b> " + optionE + "<br/>\n"
        questionContent += "<input type='hidden' name='E" + str(i) + "' value='"+optionE+"'/>\n"
        questionContent += "Answer is : <b>" + answer + "</b><br/><br/>\n"
        questionContent += "<input type='hidden' name='answer" + str(i) + "' value='"+answer+"'/>\n"

    return dict(passageContent = passageContent, questionContent = questionContent)

@auth.requires_login()
def acceptPassage():
    passageContent = str(request.vars.passage)
    numOfQuestions = int(request.vars.num_questions)
    passageId = databaseQueries.addPassage(db, passageContent)
    for i in range(1, numOfQuestions + 1):
        question = str(request.vars["question" + str(i)])
        if(question.strip()==""):
            continue
        optionA = str(request.vars["A" + str(i)])
        optionB = str(request.vars["B" + str(i)])
        optionC = str(request.vars["C" + str(i)])
        optionD = str(request.vars["D" + str(i)])
        optionE = str(request.vars["E" + str(i)])
        answer = str(request.vars["answer" + str(i)])
        databaseQueries.addQuestion(db, passageId, question, optionA, optionB, optionC, optionD, optionE, answer)
    redirect(URL('passages','solvePassage',vars=dict(passageId = passageId)))
    return dict()