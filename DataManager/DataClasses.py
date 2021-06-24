import pandas as pd
import numpy as np
from scipy.stats import mode

from .ProcessingFunctions import getInclinations
from .Constants import *
from .BaseFeature import Feature

# Abstract classes (meant to be inherited only)
class Data():

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
        self._data = self.processData(self._dataSource)

        if not self.qualityCheck():
            print("loaded data doesn't match required format")

    ## support functions
    def computeFeatures(self):
        f = []
        for fm in self.features:
            f.append(fm(self._data))

    def addFeatures(self,features):

        if type(features)==list and all(isinstance(f,Feature) for f in features):
            self.features+=features
        elif isinstance(features,Feature):
            self.features.append(features)
        else:
            print()

    def processData(self,source):
        return pd.read_csv(self._dataSource)

    def qualityCheck(self):
        return True

class TimeseriesData(Data):

    _name = 'DefaultTimeseries'

    def __init__(self,path,parseFunc=None,name = _name,freq=None):
        Data.__init__(self,path,parseFunc)

        if freq is None:
            ts = self._data[TS_COL_NAME]
            freq = 1./mode(ts.diff().values).mode[0]

        self._freq = freq
        self._fs = 1./freq

    def qualityCheck(self):
        typeCheck = type(self._data)==pd.DataFrame
        if typeCheck:
            timeCheck = TS_COL_NAME in self._data.columns
        return typeCheck & timeCheck


class TriaxialTsData(TimeseriesData):

    _name = 'DefaultTriaxial'
    features = []

    def qualityCheck(self):
        #use base Timeseries quality check, then additional checks
        TSCheck = TimeseriesData.qualityCheck(self)

        columnsAllowed = {TS_COL_NAME,X_AXIS_COL_NAME,
                          Y_AXIS_COL_NAME,Z_AXIS_COL_NAME}

        columnsCheck = False
        indexCheck = False

        if TSCheck:
            columnsCheck = set(self._data.columns)==columnsAllowed
            indexCheck = set(self._data.columns)==columnsAllowed

        return TSCheck and (columnsCheck or indexCheck)

class DerivedData(Data):

    _name = 'DefaultProcData'
    _sourceTypes = []

    def __init__(self,source,processFunc=None,name=_name):

        if self.checkSource(source):
            Data.__init__(self,source,processFunc,name)
        else:
            print('Source type not allowed')

    def checkSource(self,source):
        return any([isinstance(source,type) for type in self._sourceTypes])


# Real, child classes (meant to be actively used in code)
class AccelData(TriaxialTsData):

    _name = 'DefaultAccel'
    features = []

class InclinationData(TimeseriesData,DerivedData):

    _name = 'DefaultInclin'
    _sourceTypes = [AccelData]

    def __init__(self,source,processFunc=None,name=_name,freq=None):
        if self.checkSource(source):
            TimeseriesData.__init__(self,source,processFunc,name,source._freq)
        else:
            print('Source type not allowed')

    def processData(self,source):
        inc = getInclinations(self._dataSource._data.loc[:,[X_AXIS_COL_NAME,Y_AXIS_COL_NAME,Z_AXIS_COL_NAME]])
        inc['Time'] = self._dataSource._data.Time
        return inc
