import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

g = 9.80665 # m per sec^2

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

def vectorsToRotation(vec1, vec2):
    """ Find the rotation that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return Rotation: scipy Rotation object from rotation matrix

    https://www.theochem.ru.nl/~pwormer/Knowino/knowino.org/wiki/Rotation_matrix.html#Vector_rotation
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    return Rotation.from_matrix(rotation_matrix)

# calculate euler angles from accel data, when magnitude close to 1g (within tolerance bounds)
def getInclinations(accelTri, accelMag = None, tol=.1, gAxis = 1, eAxis = 'xyz'):
    '''
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_euler.html
    '''

    ax = matchAxis(accelTri.shape)

    refVector = np.zeros((3,1))
    refVector[gAxis] = 1

    # function for apply method
    f = lambda x: pd.Series(vectorsToRotation(refVector,x.values).as_euler(eAxis,True),
                            index=[c for c in eAxis])

    I = accelTri.apply(f,axis=ax)

    if tol is not None:

        if accelMag is None:
            accelMag = getMagnitude(accelTri)

        dropInds = (accelMag>(1+tol)*g) | (accelMag<(1-tol)*g)
        I.loc[dropInds,:] = np.nan

    return I
