#Dead code to get intellisense to work.
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

def index():
    response.view = 'default/index.html'
    if(auth.is_logged_in()):
        redirect(URL('passages','solvePassage'))
    return dict()

def aboutUs():
    response.view = "default/aboutUs.html"
    response.title = "About Us"
    return dict()

def contactUs():
    response.view = "default/contactUs.html"
    response.title = "Contact Us"
    return dict()

def updates():
    response.view = "default/updates.html"
    response.title = "Updates"
    return dict()

def statsForMyViewOnly():
    string = ""
    rows = databaseQueries.getUserDistribution(db)
    for row in rows:
        string += "<br/>Number of people from " + str(row.auth_user.Location) + " = " + str(row._extra["COUNT(auth_user.id)"]) 
    fromDate = datetime.datetime.now() - datetime.timedelta(hours=24)
    string += "<br/> Number of Passage Instances Solved in the last 24 hours = " + str(databaseQueries.getNumberOfPassageInstancesSolved(db, fromDate))
    string += "<br/> Number of Users = " + str(databaseQueries.getNumberOfUsers(db))
    response.view = ""
    return string

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
