import pandas as pd
import numpy as np

class Participant():

    _subjID = 'DefaultID'
    _cohort = None
    _dataPath = None

    def __init__(self,path = None,id = None,**kwargs):

        if not self._checkID(id):
            print('Invalid subject ID')
            return

        self._sessions = []

        self._dataPath = path; self._subjID = id

        for arg in kwargs:
            setattr(self,arg,kwargs[arg])

        self.findSessions()

    def _checkID(self,id):
        return True

    def findSessions():
        pass

    def getFeatures(self):
        F = [s.getFeatures() for s in self._sessions]
        F = pd.concat(F,axis=0,ignore_index=True).copy()
        F['Session'] = [s._name for s in self._sessions]
        return F

class Adult(Participant):

    _age = np.nan
    _ageUnits = None

    def __init__(self,path=None,id = None,**kwargs):

        Participant.__init__(self,path,id,**kwargs)

        for arg in kwargs:
            setattr(self,arg,kwargs[arg])

class Infant(Participant):

    _relDOB = np.timedelta64(0)

    def __init__(self,path=None,id = None,**kwargs):

        Participant.__init__(self,path,id,**kwargs)

        for arg in kwargs:
            setattr(self,arg,kwargs[arg])
