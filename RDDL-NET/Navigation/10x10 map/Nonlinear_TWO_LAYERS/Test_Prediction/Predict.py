from keras.models import load_model
import numpy as np
import os
import pandas as pd
from keras import backend as K
from numpy import genfromtxt

#Given local path, find full path
def PathFinder(path):
    script_dir = os.path.dirname('__file__')
    fullpath = os.path.join(script_dir,path)
    return fullpath

#Read Data for Deep Learning
def ReadData(path):
    fullpath=PathFinder(path)
    return pd.read_csv(fullpath, sep=',', header=0)

#Input Normalization
def Normalize(features, mean = [], std = []):
    if mean == []:
		mean = np.mean(features, axis = 0)
		std = np.std(features, axis = 0)
    new_feature = (features.T - mean[:,None]).T
    new_feature = (new_feature.T / std[:,None]).T
    new_feature[np.isnan(new_feature)]=0
    return new_feature, mean, std

def boosted_mean_squared_error(y_true, y_pred):
	return K.mean(K.square(y_pred - y_true)*1, axis=-1)

Label = ReadData('../Navigation_Label.txt')
Full_Label = Label.as_matrix()

PD_Data = ReadData('../Navigation_Data.txt')
Full_Data = PD_Data.as_matrix()

m_data, n_data = Full_Data.shape
Test_Data = Full_Data[int(m_data*0.9):]

print '- Data: ' + str(Full_Data[0,1])
print '- Label: ' + str(Full_Label[0,1])

TM = load_model('../TransitionModel.h5', custom_objects={'boosted_mean_squared_error': boosted_mean_squared_error})
normalized_data, mean, std = Normalize(Test_Data)
predicted = TM.predict(normalized_data)
print '\n-> Predicted Value: ' + str(predicted[0,1])
