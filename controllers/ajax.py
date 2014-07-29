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

def getQuestionCode():
    questionNumber = request.vars.questionNumber
    question = str(request.vars.question)
    optionA = str(request.vars.optionA)
    optionB = str(request.vars.optionB)
    optionC = str(request.vars.optionC)
    optionD = str(request.vars.optionD)
    optionE = str(request.vars.optionE)
    answer = str(request.vars.answer)
    htmlCode = ""
    if(utilityFunctions.checkIfVariableIsInt(questionNumber)):
        htmlCode = utilityFunctions.getQuestionInputHtmlCode(questionNumber, question, optionA, optionB, optionC, optionD, optionE, answer)
    return htmlCode