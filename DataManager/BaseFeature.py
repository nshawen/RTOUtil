import numpy as np

# generic feature class
# abstract class (for inheritance only)
class Feature:

    _sourceTypes = None
    _name = 'DefaultFeature'
    # default feature value
    _value = np.nan
    _dataSource = None

    def __init__(self,dataSource):

        self._dataSource = dataSource

        self._name = '_'.join([dataSource._name, self._name])

        if any([isinstance(dataSource,dataType) for dataType in self._sourceTypes]):
            self._value = self.calcFeature()
        else:
            print('Data source provided not compatible with this feature')

    def calcFeature(self):

        return np.nan
