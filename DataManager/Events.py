import numpy as np

class Timepoint():

    _subjID = None
    _time = np.datetime64('NaT')
    _timeRef = np.datetime64('NaT')

    _events = []
    _data = []

    def __init__(self,data={},events={},time=np.datetime64('NaT'),ref=np.datetime64('NaT')):

        self._time = time; self._timeRef = ref

        self.addData(data)
        self.addEvents(events)

    def addData(self,dataDict):

        for name in dataDict.keys():

            self._data.append(dataDict[name](self))

    def addEvents(self,eventDict):

        for name in eventDict.keys():

            self._events.append(eventDict[name](self))


class Event():

    _parentTimepoint = None

    def __init__(self,timepoint,data={}):

        self._parentTimepoint = timepoint

        self.addData(data)

    def addData(self,dataDict):

        for name in dataDict.keys():

            self._data.append(dataDict[name](self))
