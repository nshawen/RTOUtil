import pandas as pd
import numpy as np
import ProcessingFunctions as PF

# Abstract classes (meant to be inherited only)
def class Data:

    _name = 'DefaultData'
    features = []

    def __init__(self,source,processFunc==None):
        # store data filepath and parsing function that user provided
        self._dataSource = source

        # update processData function if given by user
        if processFunc is not None:
            self.processData = processFunc

        # take in and process data source
        self.parseData()

        if not self.qualityCheck():
            print("loaded data doesn't match required format")

    ## support functions
    def computeFeatures(self):
        f = []
        for fm in self.features:
            f.append(fm(self._data))

    def processData(self):
        self._data = pd.read_csv(self._dataSource)

    def qualityCheck(self):
        return True

def class TimeseriesData(Data):
    def __init__(self,path,parseFunc,freq):
        Data.__init__(self,path,parseFunc)

        self._freq = freq
        self._fs = 1./freq

# def class ProcessedData(Data):
#     def __init__(self,source,parseFunc):
#         Data.__init__(self,source,parseFunc)
#         self.processData()
#
#     def processData(self):
#         self._data = self._data

# Real, child classes (meant to be actively used in code)

def class AccelData(TimeseriesData):

    _name = 'DefaultAccel'
    features = []

    def qualityCheck(self):


def class InclinationData(TimeseriesData):

    _name = 'DefaultInclin'

    def __init__(self,source):
        TimeseriesData.__init__(self,sourcepath)
        self.processData()

    def processData(self):
        self._data = pd.apply(self._data, lambda x: np.atan2(x.xl_x,x.xl_y))
