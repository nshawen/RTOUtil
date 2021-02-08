import pickle
import os
from pathlib import Path

def pickleSave(name, data):
    with open(name, 'wb') as handle:
         pickle.dump(data, handle)
            
def pickleLoad(name):
    with open(name, 'rb') as handle:
         return pickle.load(handle)

def setLocalPath(name):
    filename = name+'.pkl'
    if os.path.exists(filename):
        return pickleLoad(filename)
    else:
        print('Input desired path')
        savepath = Path(input())
        pickleSave(filename, savepath)
        return savepath
    
    