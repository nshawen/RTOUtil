import numpy as np

# generic feature class
# abstract class (for inheritance only)
class Feature:

    _sourceTypes = ()
    _name = 'DefaultFeature'
    # default feature value
    _value = None
    _dataSource = None

    def __init__(self,dataSource,**kwargs):

        self._dataSource = dataSource

        # set all other passed attributes
        for arg in kwargs:
            setattr(self,arg,kwargs[arg])

        self.addNamePrefix()

        if self.validateSources():
            self._value = self.calcFeature()

    def calcFeature(self):

        return self.featureFunc()

    def validateSources(self):

        if any([isinstance(self._dataSource,dataType) for dataType in self._sourceTypes]):
            return True
        else:
            print('Data source provided not compatible with this feature')
            return False

    def addNamePrefix(self):

        self._name = '_'.join([self._dataSource._name, self._name])

    def featureFunc(self):

        return np.nan
