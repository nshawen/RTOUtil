import pandas as pd
import numpy as np
import scipy.stats as stats
import DataClasses as DC
import Constats as C

def getDF_Line(df,axis,line):

    if type(line)==str:
        if axis==0:
            return df.loc[line,:]
        elif axis==1:
            return df.loc[:,line]
    elif type(line)==int:
        if axis==0:
            return df.iloc[line,:]
        elif axis==1:
            return df.iloc[:,line]

    return None

# generic feature class
# abstract class (for inheritance only)
def class Feature:

    _sourceTypes = None
    _name = 'DefaultFeature'
    # default feature value
    _value = np.nan
    _dataSource = None

    def __init__(self,dataSource):

        self._dataSource = dataSource

        self._name = '_'.join([dataSource._name, self._name])

        if type(dataSource) in sourceTypes:
            self._value = self.calcFeature()
        else:
            print('Data source provided not compatible with this feature')

    def calcFeature(self):

        return np.nan

# abstract class for timeseries-based features
def class TimeseriesFeature(Feature):

    _sourceTypes = [DC.TimeseriesData]
    _name = 'TS_DefaultFeature'

    def __init__(self,dataSource,axis=0,line=0):

        # store axis/column info for feature calculation
        self._axis = axis
        self._line = line

        # store source info and calculate feature
        Feature.__init__(self,dataSource)

        # update base name to include and field name
        self._name = '_'.join([self._name, str(self._line)])

    def calcFeature(self):

        vals = getDF_Line(self._dataSource._data,self._axis,self._line).values
        ts = getDF_Line(self._dataSource._data,self._axis,C.TS_COL_NAME).values

        return self.featureFunc(vals,ts)

    # feature function taking in one row of values and corresponding timestamps
    # outputs feature value
    # meant to be overridden in inheriting classes
    def featureFunc(vals,ts):

        return np.nan

# more specific feature classes
def class Mean(TimeseriesFeature):

    _name = 'Mean'

    def featureFunc(vals,ts):

        return np.nanmean(vals)

def class StdDev(TimeseriesFeature):

    _name = 'StdDev'

    def featureFunc(vals,ts):

        return np.nanstd(vals)

def class Skewness(TimeseriesFeature):

    _name = 'Skew'

    def featureFunc(vals,ts):

        return stats.skewness(vals,nan_policy='omit')

def class Kurtosis(TimeseriesFeature):

    _name = 'Kurt'

    def featureFunc(vals,ts):

        return stats.kurtosis(vals,nan_policy='omit')
