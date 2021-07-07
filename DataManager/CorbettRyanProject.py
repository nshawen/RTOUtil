import os
import pandas as pd
from .Participants import Infant
from .Events import Session, Event
from .DataClasses import AccelData, GyroData, InclinationData
from .Features import Mean, StdDev, Skewness, Kurtosis, TimeseriesFeature
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
                featList += [feat(data,axis=0,line=c) for c in data._data.columns]
            elif issubclass(feat,Feature):
                featList += [feat(data)]
            else:
                # todo: improve warning/error messaging
                print("Input is not a valid feature class")

    data._addFeatures(featList)

def loadAccel(path,key):

    data = pd.read_hdf(path,key=key)
    data = data.loc[:,['time(ms)','xl_x','xl_y','xl_z']]
    data.rename(columns = {'time(ms)':'Time','xl_x':'X','xl_y':'Y','xl_z':'Z'},inplace=True)
    data.set_index('Time',inplace=True)

    return data

def loadGyro(path,key):

    data = pd.read_hdf(path,key=key)
    data = data.loc[:,['time(ms)','gy_x','gy_y','gy_z']]
    data.rename(columns = {'time(ms)':'Time','gy_x':'X','gy_y':'Y','gy_z':'Z'},inplace=True)
    data.set_index('Time',inplace=True)

    return data

def findData_Event(event):

    path = event._dataPath

    ds = pd.HDFStore(path)
    keys = [k for k in ds.keys() if event._name in k]
    sensors = [k.split('/')[2] for k in keys]
    ds.close()

    for k,s in zip(keys,sensors):
        event._data.append(AccelData(path,event,_processData=lambda x: loadAccel(x,k),name='_'.join(['Accel',event._name,s])))
        event._data.append(InclinationData(event._data[-1],event,name='_'.join(['Inclin',event._name,s])))
        event._data.append(GyroData(path,event,_processData=lambda x: loadGyro(x,k),name='_'.join(['Gyro',event._name,s])))

    for d in event._data:
        mountFeatures(d,[Mean,StdDev,Skewness,Kurtosis])

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

        files = [f for f in os.listdir(self._dataPath) if self._subjID in f]
        print(self._subjID,files)

        for f in files:
            try:
                name = f.replace('_','.').split('.')[1]
                self._sessions.append(Session(self,_dataPath=self._dataPath/f,_name=name))
            except:
                continue

        for s in self._sessions:
            findEvents(s)
