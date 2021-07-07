import pandas as pd
import numpy as np

class Session():

    _participant = None
    # datetime/timedelta indicating when session occured
    # reference datetime _timeRef needed for timedelta _time values
    _time = np.datetime64('NaT')
    _timeRef = np.datetime64('NaT')
    _dur = np.timedelta64(0)
    _name = 'DefaultSession'
    _dataPath = None

    def __init__(self,part,**kwargs):

        self._participant = part
        self._events = []
        self._data = []

        for arg in kwargs:
            setattr(self,arg,kwargs[arg])

    def getFeatures(self):
        F = [e.getFeatures() for e in self._events]
        F = pd.concat(F,axis=1)
        F['Session'] = self._name
        return F

class Event():

    _name = 'DefaultEvent'
    _dataPath = None
    _parentSession = None
    _startTime = np.datetime64('NaT')
    _endTime = np.datetime64('NaT')
    _eventTime = np.datetime64('NaT')
    _window = np.timedelta64(0)

    def __init__(self,session,**kwargs):

        self._data = []
        self._parentSession = session

        for arg in kwargs:
            setattr(self,arg,kwargs[arg])

    def getFeatures(self):
        F = [d.getFeatures() for d in self._data]
        F = pd.concat(F,axis=1)
        F.columns = ['_'.join([self._name,c]) for c in F.columns]
        return F
