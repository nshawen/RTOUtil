import pandas as pd
import numpy as np
import DataClasses as DC

# generic feature class
# abstract class (for inheritance only)
def class Feature:

    sourceTypes = None
    _name = 'DefaultFeature'
    # default feature value
    _value = np.nan
    _dataSource = None

    def __init__(self,dataSource):

        self._dataSource = dataSource

        if type(dataSource) in sourceTypes:
            self._value = self.calcFeature()
        else:
            print('Data source provided not compatible with this feature')

    def calcFeature(self):

        return np.nan

# more specific feature class
def class Mean(Feature)

    sourceTypes = [DC.TimeseriesData]
    name = 'Mean'

    def __init__(self,dataSource,axis=0):

        # store axis info for feature calculation
        self._axis = axis
        self._name = dataSource._name+self._name+str(axis)

        Feature.__init__(self,dataSource)

    def calcFeature(self):
