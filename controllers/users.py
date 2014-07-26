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
    redirect(URL('default','index'))
    return dict()

def login():
    if(auth.is_logged_in()):
        redirect(URL('default','index'))
    response.view = 'users/login.html'
    response.title = 'Login'
    form = auth.login()
    return dict(form=form)

def register():
    if(auth.is_logged_in()):
        redirect(URL('default','index'))
    response.view = 'users/register.html'
    response.title = 'Registration'
    
    db.auth_user["timeOfJoining"].readable = db.auth_user["timeOfJoining"].writable = False
    
    form = auth.register()
    return dict(form=form)

@auth.requires_login()
def changePassword():
    response.view = 'users/changepassword.html'
    response.title = 'Change Password'
    form = auth.change_password()
    return dict(form=form)

def retrievePassword():
    if(auth.is_logged_in()):
        redirect(URL('default','index'))
    response.view = 'users/retrievepassword.html'
    response.title = 'Retrieve Password'
    form = auth.retrieve_password()
    return dict(form = form)

def logout():
    if(auth.is_logged_in()):
        auth.logout()
    redirect(URL('default','index'))
    return dict()
