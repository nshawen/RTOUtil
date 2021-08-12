import os
import pandas as pd
import numpy as np
from .Participants import Infant
from .Events import Session, Event
from .DataClasses import AccelData, GyroData, InclinationData, MagnitudeData, XCorrData
from .Features import Mean, StdDev, Skewness, Kurtosis, TimeseriesFeature, PeakLag
from .BaseFeature import Feature

def mountFeatures(data,features):

    featList=[]

    if type(features)!=list:
        features = [features]

    for feat in features:
        #only add feature if it doesn't exist already
        if feat not in data._featureTypes:
            # identify relevant base feature type and apply feature to data
            if issubclass(feat,TimeseriesFeature):
                fs = [feat(data,axis=0,line=c) for c in data._data.columns]
                if any([f._value is not None for f in fs]):
                    featList += fs
            elif issubclass(feat,Feature):
                f = feat(data)
                if f._value is not None:
                    featList += [f]
            else:
                # todo: improve warning/error messaging
                print("Input is not a valid feature class")

    data._addFeatures(featList)

def loadAccel(self):

    data = pd.read_hdf(self._dataSource,key=self._key)
    data = data.loc[:,['time(ms)','xl_x','xl_y','xl_z']]
    data.rename(columns = {'time(ms)':'Time','xl_x':'X','xl_y':'Y','xl_z':'Z'},inplace=True)
    data.set_index('Time',inplace=True)

    return data

def loadGyro(self):

    data = pd.read_hdf(self._dataSource,key=self._key)
    data = data.loc[:,['time(ms)','gy_x','gy_y','gy_z']]
    data.rename(columns = {'time(ms)':'Time','gy_x':'X','gy_y':'Y','gy_z':'Z'},inplace=True)
    data.set_index('Time',inplace=True)

    return data

AccelData._processData = loadAccel
GyroData._processData = loadGyro

def findData_Event(event):

    path = str(event._dataPath)

    ds = pd.HDFStore(path)
    keys = [k for k in ds.keys() if event._name in k]
    sensors = [k.split('/')[2] for k in keys]
    ds.close()

    for k,s in zip(keys,sensors):
        event._data.append(AccelData(path,event,_name='_'.join(['Accel',s]),_key=k))
        event._data.append(InclinationData(event._data[-1],event,_name='_'.join(['Inclin',s])))
        event._data.append(MagnitudeData(event._data[-2],event,_name='_'.join(['AccMag',s])))
        event._data.append(GyroData(path,event,_name='_'.join(['Gyro',s]),_key=k))
        event._data.append(MagnitudeData(event._data[-1],event,_name='_'.join(['GyroMag',s])))

    # get XCorr for left/right pairs
    # won't work for <3M until location mappiung is implemented
    for k,s in zip(keys,sensors):
        if s=='S1':
            match = 'S5'
        elif s=='S2':
            match = 'S6'
        elif s=='S3':
            match = 'S7'
        elif s=='S4':
            match = 'S8'
        else:
            continue

        #find right data
        accInd = np.argmax([d._name=='_'.join(['AccMag',s]) for d in event._data])
        gyrInd = np.argmax([d._name=='_'.join(['GyroMag',s]) for d in event._data])

        accR = event._data[accInd]
        gyrR = event._data[gyrInd]

        #find left data

        accComp = [d._name=='_'.join(['AccMag',match]) for d in event._data]
        gyrComp = [d._name=='_'.join(['GyroMag',match]) for d in event._data]

        if not any(accComp) or not any(gyrComp):
            continue

        accInd = np.argmax([d._name=='_'.join(['AccMag',match]) for d in event._data])
        gyrInd = np.argmax([d._name=='_'.join(['GyroMag',match]) for d in event._data])

        accL = event._data[accInd]
        gyrL = event._data[gyrInd]

        xcorrName = '_'.join(['XCorr','Acc',s,match])
        event._data.append(XCorrData(accR,accL,'Mag','Mag',event,_name=xcorrName))

        xcorrName = '_'.join(['XCorr','Gyr',s,match])
        event._data.append(XCorrData(gyrR,gyrL,'Mag','Mag',event,_name=xcorrName))

    for d in event._data:
        mountFeatures(d,[Mean,StdDev,Skewness,Kurtosis,PeakLag])

def findEvents(session):

    path = session._dataPath

    ds = pd.HDFStore(path)
    events = set([k.split('/')[1] for k in ds.keys()])
    ds.close()

    for e in events:
        session._events.append(Event(session,_name=e,_dataPath=session._dataPath))

    for e in session._events:
        findData_Event(e)

class Corbett(Infant):

    def findSessions(self):

        files = [f for f in os.listdir(self._dataPath) if (self._subjID in f) and ('3M' in f)]
        print(self._subjID,files)

        for f in files:
            try:
                name = f.replace('_','.').split('.')[1]
                self._sessions.append(Session(self,_dataPath=self._dataPath/f,_name=name))
            except:
                continue

        for s in self._sessions:
            findEvents(s)
