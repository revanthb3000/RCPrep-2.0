#Dead code to get intellisense to work.
from applications.HereIsMyTake.modules import utilityFunctions
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
import datetime

def index(): return dict(message="hello from passages.py")

def solvePassage():
    response.view = 'passages/solvePassage.html'
    response.title = "Solve A Passage"
    response.ignoreHeading = True
    
    passageId = request.vars.passageId
    passageContent = ""
    questionContent = ""
    if(not(utilityFunctions.checkIfVariableIsInt(passageId))):
        passageId = 5
        passageContent = databaseQueries.getPassage(db, passageId)
        #Generate random Passage
    else:
        passageContent = databaseQueries.getPassage(db, passageId)
        questions = databaseQueries.getQuestions(db, passageId)
        count = 1
        for question in questions:
            questionContent += str(count) + "."
            questionContent += question.question + "<br/>"
            questionContent += "A) " + (question.optionA if question.optionA!="" else "---") + "<br/>"
            questionContent += "B) " + (question.optionB if question.optionB!="" else "---") + "<br/>"
            questionContent += "C) " + (question.optionC if question.optionC!="" else "---") + "<br/>"
            questionContent += "D) " + (question.optionD if question.optionD!="" else "---") + "<br/>"
            questionContent += "E) " + (question.optionE if question.optionE!="" else "---") + "<br/>"
            questionContent += "Answer : Option " + question.answer + "<br/><br/>"
            count += 1
        #Generate passage with id = passageId
    
    return dict(passageContent = passageContent, questionContent = questionContent)