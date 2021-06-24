from .BaseFeature import Feature
from .Features import TimeseriesFeature

__all__ = ['mountFeatures']

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
