import pandas as pd
import numpy as np
import DataClasses as DC

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
def class Mean(Feature):

    sourceTypes = [DC.TimeseriesData]
    name = 'Mean'

    def __init__(self,dataSource,axis=0,line=0):

        # store axis/column info for feature calculation
        self._axis = axis
        self._line = line
        self._name = dataSource._name+self._name+str(column)

        # store source info and calculate feature
        Feature.__init__(self,dataSource)

    def calcFeature(self):

        vals = getDF_Line(self._dataSource,self._axis,self._line).values

        return np.nanmean(vals)
