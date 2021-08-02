import numpy as np

# generic feature class
# abstract class (for inheritance only)
class Feature:

    _sourceTypes = ()
    _name = 'DefaultFeature'
    # default feature value
    _value = np.nan
    _dataSource = None

    def __init__(self,dataSource,**kwargs):

        self._dataSource = dataSource

        # set all other passed attributes
        for arg in kwargs:
            setattr(self,arg,kwargs[arg])

        addNamePrefix(self)

        if validateSources():
            self._value = self.calcFeature()

    def calcFeature(self):

        return np.nan

    def validateSources(self):

        if any([isinstance(dataSource,dataType) for dataType in self._sourceTypes]):
            return True
        else:
            print('Data source provided not compatible with this feature')
            return False

    def addNamePrefix(self):

        self._name = '_'.join([dataSource._name, self._name])
