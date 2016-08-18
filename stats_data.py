#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function  # Python 2 users only
import argparse
import pandas as pd
import numpy as np
import tensorflow.contrib.learn as skflow
from sklearn import metrics,preprocessing, linear_model


def give_data(path_train,path_test):
    train_types = {'Semana':np.uint8,'Agencia_ID':np.uint16, 'Ruta_SAK':np.uint16, 'Cliente_ID':np.uint32,'Producto_ID':np.uint16, 'Demanda_uni_equil':np.uint32}

    test_types = {'Semana':np.uint8,'Agencia_ID':np.uint16, 'Ruta_SAK':np.uint16, 'Cliente_ID':np.uint32,
                      'Producto_ID':np.uint16, 'id':np.uint16}
    df_train = pd.read_csv(path_train, usecols=train_types.keys(), dtype=train_types)
    df_test = pd.read_csv(path_test,usecols=test_types.keys(), dtype=test_types)
    return df_train,df_test
def temp_preproc_weeks(dataframe,size=None):
    weeks=[]
    for i in np.unique(dataframe.Semana):
        if size:
            weeks.append(df_train[dataframe.Semana==i].sample(size).apply(lambda x: x.astype("float64")))#convert uint32 to TensorFlow DType
    return weeks
def preproc_weeks(dataframe):
    weeks=[]
    for i in np.unique(dataframe.Semana):
        weeks.append(df_train[dataframe.Semana==i].apply(lambda x: x.astype("float64")))#convert uint32 to TensorFlow DType
        #TODO:ORDER DATA by cliente,ruta,producto; Weeks have diferent sizes
    return weeks
"""def data_preproces(weeks,logsize):
    features=[]
    labels=[]
    for i in  range(len(weeks)-logsize-1):
        weeks[i]=pd.concat(weeks[i:(i+logsize)],axis=1)
    return weeks
    PROBLEMA AL CONCATENAR
    """
def data_preproces(weeks,logsize):
    #dataframe to matrix
    for i in range(len(weeks)):
        weeks[i]=weeks[i].as_matrix()
    features=[]
    labels=[]#TODO implement with numpy
    for i in range(len(weeks)-logsize):
        weeks[i]=np.concatenate(weeks[i:(i+logsize)], axis=1)
        #weeks[i]=np.concatenate([weeks[i],weeks[i+logsize][][:-1]],axis=1)
        for j in range(len(weeks[i])):
            #print (weeks[i][j])
            #print (weeks[i+logsize][j][:-1])
            feature=np.concatenate([weeks[i][j],weeks[i+logsize][j][:-1]])
            features.append(feature)
            labels.append(weeks[i+logsize][j][-1])
        print (weeks[i])
    del weeks
    #print (features)
    #print (labels)
    return np.array(features),np.array(labels)

def model(features,labels,test_size):
    features = preprocessing.StandardScaler().fit_transform(features)
    regressor = skflow.TensorFlowLinearRegressor()
    regressor.fit(features[:-test_size], labels[:-test_size])
    preds=regressor.predict(features[-test_size:])
    print(preds[:2],labels[-test_size:][:2])
    score = metrics.mean_squared_error(preds, labels[-test_size:])
    print ("MSE: ")
    print (score)
    return regressor


def model2(features,labels,test_size):
    features = preprocessing.StandardScaler().fit_transform(features)
    regressor = linear_model.LinearRegression()
    regressor.fit(features[:-test_size], labels[:-test_size])
    preds=regressor.predict(features[-test_size:])
    print(preds[:2],labels[-test_size:][:2])
    score = metrics.mean_squared_error(preds, labels[-test_size:])
    print ("MSE: ")
    print (score)
    return regressor




if __name__ == '__main__':
    p = argparse.ArgumentParser("Statistics data")
    p.add_argument("--train",default="data/train.csv",
            action="store", dest="train",
            help="Train file [train.csv]")
    p.add_argument("--test",default="data/test.csv",
            action="store", dest="test",
            help="Train file [test.csv]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")

    opts = p.parse_args()
    print("Reading data...")
    df_train,df_test=give_data(opts.train,opts.test)
    print ("All data readed...")
    weeks=temp_preproc_weeks(df_train,2000000)
    #weeks=preproc_weeks(df_train)
    features,labels=data_preproces(weeks,3)
    print ("Starting train")
    model2(features,labels,20000)
    print ("END :D!")
