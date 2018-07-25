import random
import os
import json
import sys
import string
import unicodedata
from tqdm import tqdm
import pandas as pd

import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from scipy.spatial import distance

from shapely.geometry import Point
from shapely.geometry import MultiPoint
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import box
from shapely.geometry.polygon import LinearRing
from descartes.patch import PolygonPatch

class RandomWalk(object):
    def __init__(self, ranges):
        self.ranges=ranges
    
    def Go(self,epsilon):
        stride=[]
        for i in range(2):
            stride.append(random.uniform(self.ranges[0],self.ranges[1]))
        return stride
    
    def GoPlus(self, state):
        SampleSet=[]
        z=0
        for i in range(5):
            stride=[] 
            for j in range(2):
                stride.append(random.uniform(self.ranges[0],self.ranges[1]))#2-norm resampling
            value=np.linalg.norm([sum(x) for x in zip(stride, state[:2])])
            z=z+value
            SampleSet.append([stride[0],stride[1],value])
        SampleSet=np.array(SampleSet)
        for i in range(len(SampleSet)):
            SampleSet[i,2]=SampleSet[i,2]/z
        finalsample=np.nonzero(np.random.multinomial(1, SampleSet[:,2], size=1)==1)[1][0]
        return [SampleSet[finalsample,0],SampleSet[finalsample,1]]