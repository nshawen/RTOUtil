# Abstract classes (meant to be inherited only)
def class Data:

    dataType = None
    featureMethods = []

    def __init__(self,path):
        # store data filepath that user provided
        self.dataPath = path
        # load data from file
        self.data = self.readData(self.dataPath)

    def readData(self,path):
        self.data = pd.read_csv(path)

    def computeFeatures(self):
        f = []
        for fm in featureMethods:
            f.append(fm(self.data))

def class TimeseriesData(Data):
    def __init__(self,path,freq):
        Data.__init__(self,path)

        self.freq = freq
        self.fs = 1./freq

def class ProcessedData(Data):
    def __init__(self,sourcepath):
        Data.__init__(self,sourcepath)
        self.processData()

    def processData(self):
        self.data = self.data

# Real, child classes (meant to be actively used in code)

def class AccelData(TimeseriesData):

    dataType = 'Accel'
    featureMethods = [np.mean,np.std]

    def readData(self,path)
        pd.read_csv(path,header=0,names=['xl_x','xl_y','xl_z'])

def class InclinationData(TimeseriesData,ProcessedData):

    dataType = 'Inclination'

    def __init__(self,sourcepath):
        TimeseriesData.__init__(self,sourcepath)
        self.processData()

    def processData(self):
        self.data = pd.apply(self.data, lambda x: np.atan2(x.xl_x,x.xl_y))

def class FeatureData:
    def __init__():
