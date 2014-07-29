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

def getResultsHTMLCode(db, passageId, answers):
    htmlCode = ""
    htmlCode += "<table class='ResultTable'>\n"
    htmlCode += "<tr><td>Question</td>\n"
    htmlCode += "<td>Your Answer</td>\n"
    htmlCode += "<td>Correct Answer</td>\n"
    htmlCode += "<td>Result</td></tr>\n"
    questions = databaseQueries.getQuestions(db, passageId)
    count = 1
    numCorrect = 0
    for question in questions:
        correctAnswer = question.answer
        givenAnswer = answers[count - 1]
        if(givenAnswer==None):
            givenAnswer = "Not Answered"
        isCorrect = True if(correctAnswer == givenAnswer) else False
        if(isCorrect):
            numCorrect += 1
        score = str(IMG(_src= URL('static','images/correct.png'),_alt="Correct") if(isCorrect) else IMG(_src= URL('static','images/wrong.png'),_alt="Wrong"))
        
        htmlCode += "<tr>\n"
        htmlCode += "<td>" + str(count) + "</td>\n"
        htmlCode += "<td>" + givenAnswer + "</td>\n"
        htmlCode += "<td>" + correctAnswer + "</td>\n"
        htmlCode += "<td>" + score + "</td>\n"
        htmlCode += "</tr>\n"

        count += 1
    htmlCode += "</table><br/>\n"
    htmlCode += "<div align='center'>Your total score is : <b>" + str(numCorrect) + "/" + str(count-1) + " </b></div><br/>"
    return htmlCode

def getResultsReviewHTMLCode(db, passageId, answers):
    htmlCode = ""
    questions = databaseQueries.getQuestions(db, passageId)
    count = 1
    for question in questions:
        htmlCode += str(count) + ". "
        htmlCode += question.question + "<br/>"
        correctAnswer = question.answer
        givenAnswer = answers[count - 1]
        isCorrect = True if(correctAnswer == givenAnswer) else False
        
        colors = {}
        colors["A"] = "FFFFFF"
        colors["B"] = "FFFFFF"
        colors["C"] = "FFFFFF"
        colors["D"] = "FFFFFF"
        colors["E"] = "FFFFFF"

        colors[givenAnswer] = "ED534F" #Red
        colors[correctAnswer] = "F7E259" #Yellow
        if(isCorrect):
            colors[givenAnswer] = "73D549" #Green 
            
        
        htmlCode+="<font style='BACKGROUND-COLOR: #" + colors["A"]  + "'>"
        htmlCode += "<b>(A)</b> " + (question.optionA if question.optionA!="" else "---")
        htmlCode+="</font><br/>"
        
        htmlCode+="<font style='BACKGROUND-COLOR: #" + colors["B"]  + "'>"
        htmlCode += "<b>(B)</b> " + (question.optionB if question.optionB!="" else "---")
        htmlCode+="</font><br/>"
        
        htmlCode+="<font style='BACKGROUND-COLOR: #" + colors["C"]  + "'>"
        htmlCode += "<b>(C)</b> " + (question.optionC if question.optionC!="" else "---")
        htmlCode+="</font><br/>"
        
        htmlCode+="<font style='BACKGROUND-COLOR: #" + colors["D"]  + "'>"
        htmlCode += "<b>(D)</b> " + (question.optionD if question.optionD!="" else "---")
        htmlCode+="</font><br/>"
        
        htmlCode+="<font style='BACKGROUND-COLOR: #" + colors["E"]  + "'>"
        htmlCode += "<b>(E)</b> " + (question.optionE if question.optionE!="" else "---")
        htmlCode+="</font><br/><br/>"

        count += 1
    return htmlCode

def updateStats(db, passageId, userId, timeTaken, answers):
    questions = databaseQueries.getQuestions(db, passageId)
    score = 0
    count = 1
    for question in questions:
        correctAnswer = question.answer
        givenAnswer = answers[count - 1]
        if(givenAnswer == None):
            givenAnswer = "N/A"
        databaseQueries.insertAnswerStats(db, question.id, userId, givenAnswer)
        score += 1 if(correctAnswer == givenAnswer) else 0
        count += 1
    databaseQueries.insertPassageStats(db, passageId, userId, timeTaken, score)
        
def getQuestionInputHtmlCode(questionNumber, question, optionA, optionB, optionC, optionD, optionE, answer):
    questionNumber = str(questionNumber)
    htmlCode = ""
    htmlCode += "<textarea name='question" + questionNumber + "' style='width:93%;height:20px' placeholder=\"Q" + questionNumber + " : Enter the question here.\">"+question+"</textarea>\n"
    htmlCode += "<textarea name='A" + questionNumber + "' style='width:93%;height:20px' placeholder=\"Enter option A\">"+optionA+"</textarea>\n"
    htmlCode += "<textarea name='B" + questionNumber + "' style='width:93%;height:20px' placeholder=\"Enter option B\">"+optionB+"</textarea>\n"
    htmlCode += "<textarea name='C" + questionNumber + "' style='width:93%;height:20px' placeholder=\"Enter option C\">"+optionC+"</textarea>\n"
    htmlCode += "<textarea name='D" + questionNumber + "' style='width:93%;height:20px' placeholder=\"Enter option D\">"+optionD+"</textarea>\n"
    htmlCode += "<textarea name='E" + questionNumber + "' style='width:93%;height:20px' placeholder=\"Enter option E\">"+optionE+"</textarea>\n"
    htmlCode += "Answer :\n"
    htmlCode += "<select name='answer" + questionNumber + "'>\n"
    htmlCode += "<option value='A' " + ("selected" if(answer=="A") else "") + ">A</option>\n"
    htmlCode += "<option value='B' " + ("selected" if(answer=="B") else "") + ">B</option>\n"
    htmlCode += "<option value='C' " + ("selected" if(answer=="C") else "") + ">C</option>\n"
    htmlCode += "<option value='D' " + ("selected" if(answer=="D") else "") + ">D</option>\n"
    htmlCode += "<option value='E' " + ("selected" if(answer=="E") else "") + ">E</option>\n"
    htmlCode += "</select><br/><br/>\n"
    return htmlCode