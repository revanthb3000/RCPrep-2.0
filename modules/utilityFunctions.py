#!/usr/bin/env python
# coding: utf8
from gluon import *

def checkIfVariableIsInt(var):
    try:
        x = int(var)
    except:
        return False
    return True