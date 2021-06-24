from .BaseFeature import Feature
from .Features import TimeseriesFeature

__all__ = ['mountFeatures']

def mountFeatures(data,features):

    if type(features)!=list:
        features = [features]

    for feature in features:
        if issubclass(feature,TimeseriesFeature):
            featureList = [feature(data,axis=0,line=c) for c in data._data.columns]
        elif issubclass(feature,Feature):
            featureList = [feature(data)]
        else:
            # todo improve warning/error messaging
            print("Input is not a valid feature class")
            featureList=[]

        data.addFeatures(featureList)
