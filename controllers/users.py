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

def index(): return dict(message="hello from users.py")