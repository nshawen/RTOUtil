import pandas as pd
import numpy as np
from scipy.stats import mode
from scipy.signal import correlate, correlation_lags

from .ProcessingFunctions import getInclinations, getMagnitude
from .Constants import *
from .BaseFeature import Feature

# Abstract classes (meant to be inherited only)
class Data():

    _name = 'DefaultData'
    _dataSource = None
    _dataContext = None

    def __init__(self,source,context,**kwargs):
        # store data source and context (required inputs)
        self._dataSource = source
        self._dataContext = context
        # these need to be instance variables because they are mutable
        self._features = []
        self._featureTypes = set()

        # set all other passed attributes
        for arg in kwargs:
            setattr(self,arg,kwargs[arg])

        # take in and process data source
        self._data = self._processData()

        if not self._qualityCheck():
            print("loaded data doesn't match required format")

    def _addFeatures(self,features):

        if type(features)==list and all(isinstance(f,Feature) for f in features):
            self._features+=features
            for f in features: self._featureTypes.add(type(f))
        elif isinstance(features,Feature):
            self._features.append(features)
            self._featureTypes.add(type(features))
        else:
            print('Invalid data types present')

    def _processData(self):
        return pd.read_csv(self._dataSource)

    def _qualityCheck(self):
        return True

    def getFeatures(self):
        vals = [f._value for f in self._features]
        names = [f._name for f in self._features]
        F = pd.DataFrame(index=[0],columns=names,data=np.array(vals).reshape((1,-1)))
        return F

class TimeseriesData(Data):

    _name = 'DefaultTimeseries'
    _freq = np.nan
    _fs = np.nan
    _interp = False

    def __init__(self,source,context,**kwargs):
        Data.__init__(self,source,context,**kwargs)

        # pull freq data from original signal
        if self._freq is np.nan:
            ts = self._data.index
            if len(ts)>0:
                self._freq = 1./mode(np.diff(ts)).mode[0]

        self._fs = 1./self._freq

    def _qualityCheck(self):
        typeCheck = type(self._data)==pd.DataFrame

        timeCheck = False
        if typeCheck:
            timeCheck = self._data.index.name==TS_COL_NAME
        return typeCheck & timeCheck


class TriaxialTsData(TimeseriesData):

    _name = 'DefaultTriaxial'

    def _qualityCheck(self):
        #use base Timeseries quality check, then additional checks
        tsCheck = TimeseriesData._qualityCheck(self)

        columnsAllowed = {X_AXIS_COL_NAME,Y_AXIS_COL_NAME,Z_AXIS_COL_NAME}

        columnsCheck = False
        indexCheck = False

        if tsCheck:
            columnsCheck = set(self._data.columns)==columnsAllowed
            indexCheck = set(self._data.columns)==columnsAllowed

        return tsCheck and (columnsCheck or indexCheck)

class DerivedData(Data):

    _name = 'DefaultProcData'
    # needs to be a tuple to be immutable
    # AVOID any mutable class variables to avoid odd behaviors
    _sourceTypes = ()

    def __init__(self,source,context,**kwargs):

        if self._checkSource(source):
            Data.__init__(self,source,context,**kwargs)
            # self._name = '_'.join([self._name,context._name])
        else:
            print('Source type not allowed')

    def _checkSource(self,source):
        return any([isinstance(source,validType) for validType in self._sourceTypes])


# Real, child classes (meant to be actively used in code)
class AccelData(TriaxialTsData):

    _name = 'Accel'

class GyroData(TriaxialTsData):

    _name = 'Gyro'

class InclinationData(TimeseriesData,DerivedData):

    _name = 'Inclin'
    _sourceTypes = (AccelData,)

    def __init__(self,source,context,**kwargs):

        if self._checkSource(source):
            TimeseriesData.__init__(self,source,context,**kwargs)
        else:
            print('Source type not allowed')

    def _processData(self):
        inc = getInclinations(self._dataSource._data.loc[:,[X_AXIS_COL_NAME,Y_AXIS_COL_NAME,Z_AXIS_COL_NAME]])
        return inc

class MagnitudeData(TimeseriesData,DerivedData):

    _name = 'Mag'
    _sourceTypes = (TriaxialTsData,)

    def __init__(self,source,context,**kwargs):

        if self._checkSource(source):
            TimeseriesData.__init__(self,source,context,**kwargs)
        else:
            print('Source type not allowed')

    def _processData(self):
        mag = getMagnitude(self._dataSource._data.loc[:,[X_AXIS_COL_NAME,Y_AXIS_COL_NAME,Z_AXIS_COL_NAME]])
        return pd.DataFrame(mag,columns=['Mag'])

class XCorrData(DerivedData):
    ###
    # data is DataFrame with lag in index and XCorr as values
    # currently only compatible with string columns

    _name = 'XCorr'
    _sourceTypes = (TimeseriesData,)

    def __init__(self,source1,source2,s1col,s2col,context,**kwargs):

        if self._checkSource(source1) & self._checkSource(source2):
            Data.__init__(self,(source1,source2),context,_s1col=s1col,_s2col=s2col,**kwargs)
            # self._name = '_'.join([self._name,context._name])
        else:
            print('At least one source type is not allowed')

    def _processData(self):

        source1 = self._dataSource[0]._data.loc[:,self._s1col].values
        source2 = self._dataSource[1]._data.loc[:,self._s2col].values

        lags = correlation_lags(len(source1),len(source2))
        corr = correlate(source1,source2)

        return pd.DataFrame(index=lags,data=corr)
