import pandas as pd
import numpy as np
from scipy.stats import mode

from .ProcessingFunctions import getInclinations
from .Constants import *
from .BaseFeature import Feature

# Abstract classes (meant to be inherited only)
class Data():

    _name = 'DefaultData'
    _features = []
    _featureTypes = set()

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

    def _addFeatures(self,features):

        if type(features)==list and all(isinstance(f,Feature) for f in features):
            self.features+=features
            for f in features: self._featureTypes.add(type(f))
        elif isinstance(features,Feature):
            self.features.append(features)
            self._featureTypes.add(type(features))
        else:
            print('Invalid data types present')

    def processData(self,source):
        return pd.read_csv(self._dataSource)

    def qualityCheck(self):
        return True

class TimeseriesData(Data):

    _name = 'DefaultTimeseries'

    def __init__(self,path,parseFunc=None,name = _name,freq=None):
        Data.__init__(self,path,parseFunc)

        if freq is None:
            ts = self._data.index
            freq = 1./mode(np.diff(ts)).mode[0]

        self._freq = freq
        self._fs = 1./freq

    def qualityCheck(self):
        typeCheck = type(self._data)==pd.DataFrame
        if typeCheck:
            timeCheck = self._data.index.name==TS_COL_NAME
        return typeCheck & timeCheck


class TriaxialTsData(TimeseriesData):

    _name = 'DefaultTriaxial'

    def qualityCheck(self):
        #use base Timeseries quality check, then additional checks
        tsCheck = TimeseriesData.qualityCheck(self)

        columnsAllowed = {X_AXIS_COL_NAME,Y_AXIS_COL_NAME,Z_AXIS_COL_NAME}

        columnsCheck = False
        indexCheck = False

        if tsCheck:
            columnsCheck = set(self._data.columns)==columnsAllowed
            indexCheck = set(self._data.columns)==columnsAllowed

        return tsCheck and (columnsCheck or indexCheck)

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
        return inc
