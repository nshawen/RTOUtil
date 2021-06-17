import pandas as pd
import numpy as np
import ProcessingFunctions as PF
import Features as F
import Constants as C

# Abstract classes (meant to be inherited only)
def class Data:

    _name = 'DefaultData'
    features = []

    def __init__(self,source,processFunc=None,name=_name):
        # store data filepath and name
        self._dataSource = source
        self._name = name

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
    def __init__(self,path,parseFunc=None,freq=None):
        Data.__init__(self,path,parseFunc)

        if freq is None:
            ts = self._data[C.TS_COL_NAME]
            freq = 1./np.mode(ts.diff().values)

        self._freq = freq
        self._fs = 1./freq

    def qualityCheck(self):
        typeCheck = type(self._data)==pd.DataFrame
        if typeCheck:
            timeCheck = C.TS_COL_NAME in self._data.columns
        return typeCheck & timeCheck


def class TriaxialTsData(TimeseriesData):

    _name = 'DefaultTriaxial'
    features = []

    def qualityCheck(self):
        #use base Timeseries quality check, then additional checks
        TSCheck = TimeseriesData.qualityCheck(self)

        columnsAllowed = {C.TS_COL_NAME,C.X_AXIS_COL_NAME,
                          C.Y_AXIS_COL_NAME,C.Z_AXIS_COL_NAME}

        columnsCheck = False
        indexCheck = False

        if TSCheck:
            columnsCheck = set(self._data.columns)==columnsAllowed
            indexCheck = set(self._data.columns)==columnsAllowed

        return TSCheck and (columnsCheck or indexCheck)

def class ProcessedData(Data):

    _name = 'DefaultProcData'
    _sourceTypes = []

    def __init__(self,source,processFunc=None,name=_name):

        if self.checkSource(source):
            Data.__init__(self,source,processFunc,name=)
        else:
            print('Source type not allowed')

    def checkSource(self,source):
        return type(source) in self._sourceTypes


# Real, child classes (meant to be actively used in code)
def class AccelData(TriaxialTsData):

    _name = 'DefaultAccel'
    features = []

def class InclinationData(TimeseriesData,ProcessedData):

    _name = 'DefaultInclin'

    def __init__(self,source,processFunc=None,name=_name):
        if self.checkSource(source):
            TimeseriesData.__init__(self,source,processFunc,name)
            self.processData()

    def processData(self):
        self._data = pd.apply(self._data, lambda x: np.atan2(x.xl_x,x.xl_y))
