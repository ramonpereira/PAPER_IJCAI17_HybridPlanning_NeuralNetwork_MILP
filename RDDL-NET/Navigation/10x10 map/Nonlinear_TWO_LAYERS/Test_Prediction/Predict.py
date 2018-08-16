from keras.models import load_model
import numpy as np
import os
import pandas as pd
from keras import backend as K
from numpy import genfromtxt

# Given local path, find full path (by Buser)
def PathFinder(path):
    script_dir = os.path.dirname('__file__')
    fullpath = os.path.join(script_dir,path)
    return fullpath

# Read Data for Deep Learning (by Buser)
def ReadData(path):
    fullpath=PathFinder(path)
    return pd.read_csv(fullpath, sep=',', header=0)

# Input Normalization (by Buser)
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

#
# A simple code to test the Transition Model for Navigation (10 x 10).
#
Label = ReadData('../Navigation_Label.txt')
Full_Label = Label.as_matrix()

Data = ReadData('../Navigation_Data.txt')
Full_Data = Data.as_matrix()

m_data, n_data = Full_Data.shape
Test_Data = Full_Data[int(m_data*0.9):]

print '- Data: X=' + str(Full_Data[0,0]) + ' Y=' + str(Full_Data[0,1])
print '- Label: X=' + str(Full_Label[0,0]) + ' Y=' + str(Full_Label[0,1])

TM = load_model('../TransitionModel.h5', custom_objects={'boosted_mean_squared_error': boosted_mean_squared_error})
normalized_data, mean, std = Normalize(Test_Data)

Action_Plain = pd.DataFrame([[0.3320377856738716,-0.5740284433548912,8.873047250861017,8.561600206524771]], columns=list('ABCD'))
Action_Plain_Data = Action_Plain.as_matrix()
normalized_data_action_plain = Normalize(Action_Plain_Data, mean, std)
print normalized_data_action_plain

Action = ReadData('../Action.txt')
Action_Data = Action.as_matrix()
normalized_data_action = Normalize(Action_Data, mean, std)
print normalized_data_action

print '\n- Action: X=' + str(Action_Data[0,0]) + ' Y=' + str(Action_Data[0,1])

print '\n# Mean: ' + str(mean)
print '# Std: ' + str(std)

predicted = TM.predict(normalized_data_action[0])
#predicted = TM.predict(normalized_data)
print '\n-> Predicted Value: X=' + str(predicted[0,0]) + ' Y=' + str(predicted[0,1])