import pandas as pd
import numpy as np
import scipy.stats as stats

from .DataClasses import TimeseriesData, XCorrData
from .Constants import *
from .BaseFeature import Feature

def getDF_Line(df,axis,line):

    if type(line)==str:
        if axis==0:
            return df.loc[:,line]
        elif axis==1:
            return df.loc[line,:]
    elif type(line)==int:
        if axis==0:
            return df.iloc[:,line]
        elif axis==1:
            return df.iloc[line,:]

    return None

# abstract class for timeseries-based features
class TimeseriesFeature(Feature):

    _sourceTypes = (TimeseriesData,XCorrData)
    _name = 'TS_DefaultFeature'

    def __init__(self,dataSource,axis=0,line=0,**kwargs):

        # store axis/column info for feature calculation
        self._axis = axis
        self._line = line

        # store source info and calculate feature
        Feature.__init__(self,dataSource,**kwargs)

    def calcFeature(self):

        vals = getDF_Line(self._dataSource._data,self._axis,self._line).values
        ts = self._dataSource._data.index.values

        return self.featureFunc(vals,ts)

    def addNamePrefix(self):
        # include source and field names
        self._name = '_'.join([self._dataSource._name, str(self._line), self._name])

    # feature function taking in one row of values and corresponding timestamps
    # outputs feature value
    # meant to be overridden in inheriting classes
    def featureFunc(self,vals,ts):

        return np.nan

class MultiSourceFeature(Feature):

    _dataSource = ()
    _name = 'Multi_DefaultFeature'
    _minLen = 2
    _maxLen = None

    def __init__(self,dataSources):

        self._dataSource = tuple([source for source in dataSources])

    def addNamePrefix(self):
        self._name = '_'.join([source._name for source in self._dataSource]+[self._name])

    def validateSources(self):
        if all([any([isinstance(source,dataType) for dataType in self._sourceTypes]) for source in dataSource]):
            return True
        else:
            print('A data source provided is not compatible with this feature')
            return False

# more specific feature classes
class Mean(TimeseriesFeature):

    _name = 'Mean'

    def featureFunc(self,vals,ts):

        return np.nanmean(vals)

class StdDev(TimeseriesFeature):

    _name = 'StdDev'

    def featureFunc(self,vals,ts):

        return np.nanstd(vals)

class Skewness(TimeseriesFeature):

    _name = 'Skew'

    def featureFunc(self,vals,ts):

        return stats.skew(vals,nan_policy='omit')

class Kurtosis(TimeseriesFeature):

    _name = 'Kurt'

    def featureFunc(self,vals,ts):

        return stats.kurtosis(vals,nan_policy='omit')

class PeakLag(Feature):

    _name = 'Lag@Max'
    _sourceTypes = (XCorrData,)

    def featureFunc(self):
        return self._dataSource._data.idxmax().values[0]
