#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 13:47:22 2023

@author: enora
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import xarray as xr
import random
from category_encoders.target_encoder import TargetEncoder
from sklearn.model_selection import train_test_split  
from xgboost import XGBRegressor
from sklearn.preprocessing import OneHotEncoder
import os

def training_model(model,encoder): #model = 'rf' ou 'xgb' et encoder = 'ohe' ou 'target'
    '''On peut choisir le modèle (xgboost ou random forest) ainsi que la façon d'encoder 'OneHotEncoder ou Target Encoding)'''
    
    path = os.getcwd()
    file = path+'/pricing_requests_tot.csv'  #base de données complètes

    dataset = pd.DataFrame(pd.read_csv(file))
    dataset_brut = pd.DataFrame(pd.read_csv(file))
    del dataset['Unnamed: 0']
    del dataset_brut['Unnamed: 0']

    dict_city =  dataset.groupby('city')['price'].mean().to_dict()
    dict_brand = dataset.groupby('brand')['price'].mean().to_dict()
    #dict_group = dataset.groupby('group')['price'].mean().to_dict()

    
    if encoder == 'target':
        encoder = TargetEncoder()
            
        dataset_targ = dataset
        dataset_targ['city']=encoder.fit_transform(dataset_targ['city'],dataset_targ['price'])
        dataset_targ['language']=encoder.fit_transform(dataset_targ['language'],dataset_targ['price'])
        dataset_targ['brand']=encoder.fit_transform(dataset_targ['brand'],dataset_targ['price'])
        dataset_targ['group']=encoder.fit_transform(dataset_targ['group'],dataset_targ['price'])
            
        X = dataset_targ.drop(labels='price',axis=1) 
        del X['language'] #on retire les features dont l'importance est faible (cf le notebook Analysis)
        del X['parking']
        del X['avatar_id']
        del X['children_policy']
        del X['mobile']
        del X['group']
        del X['pool']
        Y = dataset_targ.price
            
           
    elif encoder == 'ohe':
        colnames = pd.get_dummies(dataset_brut, columns = ["city","language","group","brand"]).columns
        enc=OneHotEncoder()
        enc_data=pd.DataFrame(enc.fit_transform(dataset[["city","language","group","brand"]]).toarray())
        df_ohe=dataset.join(enc_data)
        del df_ohe['city']
        del df_ohe['group']
        del df_ohe['brand']
        del df_ohe['language']

        one_hot_encoded_data = df_ohe.set_axis(list(colnames), axis=1)
        X = one_hot_encoded_data.drop(labels='price',axis=1)
        del X['language']   #on retire les features dont l'importance est faible (cf le notebook Analysis)
        del X['parking']
        del X['avatar_id']
        del X['children_policy']
        del X['mobile']
        del X['pool']
        del X['group']
        Y = one_hot_encoded_data.price

            
    else : 
        print('encodeur inconnu')
            
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.1)
    
    if model == 'xgb':
        xgb = XGBRegressor()
        xgb.fit(X_train,Y_train)
        mod = xgb
        print(f"XGBoost score: {xgb.score(X_test, Y_test):.2f}")
        
    elif model == 'rf':
        rf = RandomForestRegressor(max_depth=10)
        rf.fit(X_train, Y_train)
        mod = rf
        print(f"Random forest score: {rf.score(X_test, Y_test):.2f}")
        
    else :
        print('modèle inconnu')
    
    return(mod)

training_model('xgb','target')
