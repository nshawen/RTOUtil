import numpy as np

class Participant():

    _subjID
    _cohort = None
    _timepoints = []

    def __init__(self,timepoints={},id = None, cohort=None):

        if not self._checkID(id):
            print('Invalid subject ID')
            return

        self._subjID = id; self._cohort = cohort
        self.addData(timepoints)

    def addTimepoints(self,timepointDict):

        for name in timepointDict.keys():

            self._timepoints.append(timepointDict[name](self))

    def _checkID(self,id):

        return True

class Adult(Participant):

    _age = np.nan
    _ageUnits = None

    def __init__(self,timepoints={},id = None,cohort=None,age=np.nan,ageUnits=None):

        Participant.__init__(self,timepoints,cohort)

        self._age = age; self._ageUnits = _ageUnits

class Infant(Participant):

    _DOB = np.datetime64('NaT')
    _termDate = np.datetime64('NaT')

    def __init__(self,timepoints={},id = None,cohort=None,dob=np.datetime64('NaT'),termDate=np.datetime64('NaT')):

        Participant.__init__(self,timepoints,cohort)

        self._DOB = dob; self._termDate = _termDate
