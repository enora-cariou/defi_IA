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
import gradio as gr

def training_model(model,encoder): #model = 'rf' ou 'xgb' et encoder = 'ohe' ou 'target'
    path = os.getcwd()
    file = path+'/pricing_requests/pricing_requests_tot.csv'

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
        del X['language']
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
        del X['language']
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

#training_model('xgb','target')


def calcul_prix(city,date,stock,brand):
    path2=os.getcwd()
    #piscine = '1' if pool else '0'
    hotel_id = random.randint(0,998)
   
    file2 = path2+'/pricing_requests/pricing_requests_tot.csv'
    dataset = pd.DataFrame(pd.read_csv(file2))
    dataset_brut = pd.DataFrame(pd.read_csv(file2))
    del dataset['Unnamed: 0']
    del dataset_brut['Unnamed: 0']
    
    X_test =[(str(city),int(date),int(hotel_id),int(stock),str(brand))]
    X_test = pd.DataFrame(X_test,columns=['city','date','hotel_id','stock','brand'])
    nom_colonnes = ['hotel_id','stock','city','date','brand']
    
    dict_city_test =  dataset_brut.groupby('city')['price'].mean().to_dict()
    dict_brand_test = dataset_brut.groupby('brand')['price'].mean().to_dict()
    
    city_encoding=[]
    brand_encoding=[]

    for i in X_test['city']:
        city_encoding.append(dict_city_test[str(i)])
    for i in X_test['brand']:
         brand_encoding.append(dict_brand_test[str(i)])
    
    X_test['city_enc']=city_encoding
    X_test['brand_enc']=brand_encoding

    del X_test['city']
    del X_test['brand']

    X_test_rename = X_test.rename(columns={"city_enc": "city", "brand_enc":"brand"})
    X_test_reorder = X_test_rename[np.array(nom_colonnes)] #labels dans le bon ordre    
    
    y_pred = training_model('xgb','target').predict(X_test_reorder)  #on utilise le modèle XGBoost avec un target encodeur
    y_pred=pd.DataFrame(y_pred)
    price = round(float(y_pred[0].values[0]),2)
        
    annonce = f"On vous a trouvé une chambre à {city}, pour dans {date} jours au prix de {price} euros"
    
    return annonce

path3=os.getcwd()
hotel_features = pd.read_csv(path3+'/features_hotels.csv',index_col=['hotel_id', 'city'])
brand = hotel_features['brand'].unique()
ville = ['paris','amsterdam','madrid','copenhagen','rome','vienna','vilnius','sofia','valletta']

demo = gr.Interface(
    fn=calcul_prix,
    inputs=[gr.Dropdown(list(ville), multiselect=False),"text","text",gr.Radio(list(brand))],
    outputs=["text"],
)
demo.launch()

