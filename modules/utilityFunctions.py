#!/usr/bin/env python
# coding: utf8
from gluon import *
import random
import databaseQueries

def checkIfVariableIsInt(var):
    try:
        x = int(var)
    except:
        return False
    return True

def getRandomNumber(minValue, maxValue):
    number = random.randrange(minValue, maxValue)
    return number

def getQuestionsHTMLCode(db, passageId):
    htmlCode = ""
    questions = databaseQueries.getQuestions(db, passageId)
    count = 1
    for question in questions:
        htmlCode += str(count) + ". "
        htmlCode += question.question + "<br/>"
        htmlCode += '<input type="radio" value="A" name="question-' + str(count)+ '">' + " <b>(A)</b> " + (question.optionA if question.optionA!="" else "---") + "<br/>"
        htmlCode += '<input type="radio" value="B" name="question-' + str(count)+ '">' + " <b>(B)</b> " + (question.optionB if question.optionB!="" else "---") + "<br/>"
        htmlCode += '<input type="radio" value="C" name="question-' + str(count)+ '">' + " <b>(C)</b> " + (question.optionC if question.optionC!="" else "---") + "<br/>"
        htmlCode += '<input type="radio" value="D" name="question-' + str(count)+ '">' + " <b>(D)</b> " + (question.optionD if question.optionD!="" else "---") + "<br/>"
        htmlCode += '<input type="radio" value="E" name="question-' + str(count)+ '">' + " <b>(E)</b> " + (question.optionE if question.optionE!="" else "---") + "<br/><br/>"
        count += 1
    return htmlCode