import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

g = 9.80665 # m per sec^2

### Utilities functions ###

# check for axis of specified length and return its position
def matchAxis(shape,l=3):
    if l not in shape:
        print("No axis of length ",l)
        return None

    # find matching axis
    ax = np.where(np.array(shape)==l)[0][0]

    return ax

# magnitude calculations for triaxial signals
def getMagnitude(signal):
    ax = matchAxis(signal.shape)

    return signal.apply(lambda x: (x.iloc[0]**2+x.iloc[1]**2+x.iloc[2]**2)**.5,axis=ax)

### User-facing processing functions for use with data classes ###

def vectorsToRotation(vec1, vec2):
    ''' Find the rotation that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return Rotation: scipy Rotation object from rotation matrix

    https://www.theochem.ru.nl/~pwormer/Knowino/knowino.org/wiki/Rotation_matrix.html#Vector_rotation
    '''
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    return Rotation.from_matrix(rotation_matrix)

# calculate euler angles from accel data, when magnitude close to 1g (within tolerance bounds)
def getInclinations(accel_tri, accel_mag = None, tol=None, rel_vec = 0, e_axis = 'XYZ'):
    '''
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_euler.html
    '''

    ax = matchAxis(accel_tri.shape)

    if type(rel_vec) == int:
        refVector = np.zeros((3,1))
        refVector[rel_vec] = 1
    elif len(rel_vec) == 3:
        refVector = rel_vec
    else:
        raise Exception('Incorrect reference vector format. Should be an integer or len 3 iterable')

    # function for apply method
    f = lambda x: pd.Series(vectorsToRotation(refVector,x.values).as_euler(e_axis,True),
                            index=[c for c in e_axis])

    I = accel_tri.apply(f,axis=ax)

    if tol is not None:

        if accel_mag is None:
            accel_mag = getMagnitude(accel_tri)

        dropInds = (accel_mag>(1+tol)*g) | (accel_mag<(1-tol)*g)
        I.loc[dropInds,:] = np.nan

    return I

def getSpectrogram(signal):
    pass
