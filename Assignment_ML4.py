
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-machine-learning/resources/bANLa) course resource._
# 
# ---

# ## Assignment 4 - Understanding and Predicting Property Maintenance Fines
# 
# This assignment is based on a data challenge from the Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)). 
# 
# The Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)) and the Michigan Student Symposium for Interdisciplinary Statistical Sciences ([MSSISS](https://sites.lsa.umich.edu/mssiss/)) have partnered with the City of Detroit to help solve one of the most pressing problems facing Detroit - blight. [Blight violations](http://www.detroitmi.gov/How-Do-I/Report/Blight-Complaint-FAQs) are issued by the city to individuals who allow their properties to remain in a deteriorated condition. Every year, the city of Detroit issues millions of dollars in fines to residents and every year, many of these fines remain unpaid. Enforcing unpaid blight fines is a costly and tedious process, so the city wants to know: how can we increase blight ticket compliance?
# 
# The first step in answering this question is understanding when and why a resident might fail to comply with a blight ticket. This is where predictive modeling comes in. For this assignment, your task is to predict whether a given blight ticket will be paid on time.
# 
# All data for this assignment has been provided to us through the [Detroit Open Data Portal](https://data.detroitmi.gov/). **Only the data already included in your Coursera directory can be used for training the model for this assignment.** Nonetheless, we encourage you to look into data from other Detroit datasets to help inform feature creation and model selection. We recommend taking a look at the following related datasets:
# 
# * [Building Permits](https://data.detroitmi.gov/Property-Parcels/Building-Permits/xw2a-a7tf)
# * [Trades Permits](https://data.detroitmi.gov/Property-Parcels/Trades-Permits/635b-dsgv)
# * [Improve Detroit: Submitted Issues](https://data.detroitmi.gov/Government/Improve-Detroit-Submitted-Issues/fwz3-w3yn)
# * [DPD: Citizen Complaints](https://data.detroitmi.gov/Public-Safety/DPD-Citizen-Complaints-2016/kahe-efs3)
# * [Parcel Map](https://data.detroitmi.gov/Property-Parcels/Parcel-Map/fxkw-udwf)
# 
# ___
# 
# We provide you with two data files for use in training and validating your models: train.csv and test.csv. Each row in these two files corresponds to a single blight ticket, and includes information about when, why, and to whom each ticket was issued. The target variable is compliance, which is True if the ticket was paid early, on time, or within one month of the hearing data, False if the ticket was paid after the hearing date or not at all, and Null if the violator was found not responsible. Compliance, as well as a handful of other variables that will not be available at test-time, are only included in train.csv.
# 
# Note: All tickets where the violators were found not responsible are not considered during evaluation. They are included in the training set as an additional source of data for visualization, and to enable unsupervised and semi-supervised approaches. However, they are not included in the test set.
# 
# <br>
# 
# **File descriptions** (Use only this data for training your model!)
# 
#     readonly/train.csv - the training set (all tickets issued 2004-2011)
#     readonly/test.csv - the test set (all tickets issued 2012-2016)
#     readonly/addresses.csv & readonly/latlons.csv - mapping from ticket id to addresses, and from addresses to lat/lon coordinates. 
#      Note: misspelled addresses may be incorrectly geolocated.
# 
# <br>
# 
# **Data fields**
# 
# train.csv & test.csv
# 
#     ticket_id - unique identifier for tickets
#     agency_name - Agency that issued the ticket
#     inspector_name - Name of inspector that issued the ticket
#     violator_name - Name of the person/organization that the ticket was issued to
#     violation_street_number, violation_street_name, violation_zip_code - Address where the violation occurred
#     mailing_address_str_number, mailing_address_str_name, city, state, zip_code, non_us_str_code, country - Mailing address of the violator
#     ticket_issued_date - Date and time the ticket was issued
#     hearing_date - Date and time the violator's hearing was scheduled
#     violation_code, violation_description - Type of violation
#     disposition - Judgment and judgement type
#     fine_amount - Violation fine amount, excluding fees
#     admin_fee - $20 fee assigned to responsible judgments
# state_fee - $10 fee assigned to responsible judgments
#     late_fee - 10% fee assigned to responsible judgments
#     discount_amount - discount applied, if any
#     clean_up_cost - DPW clean-up or graffiti removal cost
#     judgment_amount - Sum of all fines and fees
#     grafitti_status - Flag for graffiti violations
#     
# train.csv only
# 
#     payment_amount - Amount paid, if any
#     payment_date - Date payment was made, if it was received
#     payment_status - Current payment status as of Feb 1 2017
#     balance_due - Fines and fees still owed
#     collection_status - Flag for payments in collections
#     compliance [target variable for prediction] 
#      Null = Not responsible
#      0 = Responsible, non-compliant
#      1 = Responsible, compliant
#     compliance_detail - More information on why each ticket was marked compliant or non-compliant
# 
# 
# ___
# 
# ## Evaluation
# 
# Your predictions will be given as the probability that the corresponding blight ticket will be paid on time.
# 
# The evaluation metric for this assignment is the Area Under the ROC Curve (AUC). 
# 
# Your grade will be based on the AUC score computed for your classifier. A model which with an AUROC of 0.7 passes this assignment, over 0.75 will recieve full points.
# ___
# 
# For this assignment, create a function that trains a model to predict blight ticket compliance in Detroit using `readonly/train.csv`. Using this model, return a series of length 61001 with the data being the probability that each corresponding ticket from `readonly/test.csv` will be paid, and the index being the ticket_id.
# 
# Example:
# 
#     ticket_id
#        284932    0.531842
#        285362    0.401958
#        285361    0.105928
#        285338    0.018572
#                  ...
#        376499    0.208567
#        376500    0.818759
#        369851    0.018528
#        Name: compliance, dtype: float32
#        
# ### Hints
# 
# * Make sure your code is working before submitting it to the autograder.
# 
# * Print out your result to see whether there is anything weird (e.g., all probabilities are the same).
# 
# * Generally the total runtime should be less than 10 mins. You should NOT use Neural Network related classifiers (e.g., MLPClassifier) in this question. 
# 
# * Try to avoid global variables. If you have other functions besides blight_model, you should move those functions inside the scope of blight_model.
# 
# * Refer to the pinned threads in Week 4's discussion forum when there is something you could not figure it out.

# In[38]:

import pandas as pd
import numpy as np

train = pd.read_csv('train.csv',encoding = 'ISO-8859-1')
test = pd.read_csv('test.csv')
train.set_index('ticket_id')
train.columns


# In[39]:

test.columns


# In[40]:

train.shape


# In[41]:

test.shape


# In[42]:

train.head()


# In[43]:

train[(train['compliance'] == 0.0) | (train['compliance'] == 1.0)].shape


# In[48]:

address = pd.read_csv('addresses.csv')
address.head()
address.shape


# In[49]:

latlons = pd.read_csv('latlons.csv')


# In[50]:

address = pd.merge(address, latlons,how ='left')
address.shape


# In[51]:

test = pd.merge(test,address,how='left')
train = pd.merge(train,address,how='left')
test.shape


# In[52]:

train_df= train[(train['compliance'] == 0.0) | (train['compliance'] == 1.0)]
train_df.shape


# In[53]:

train_df = train_df[~train_df['hearing_date'].isnull()]


# In[54]:

train_df.shape


# feature_to_be_splitted = ['agency_name', 'state', 'disposition']
# train_df = pd.get_dummies(train_df,columns=feature_to_be_splitted)
# test = pd.get_dummies(test,columns=feature_to_be_splitted)
# train_df.shape

# In[55]:

train_drop_list=['balance_due','payment_amount','payment_date','payment_status' ,'collection_status' ,'compliance_detail']
train_df.drop(train_drop_list,axis=1,inplace = True)


# In[56]:

string_list = ['violator_name', 'zip_code', 'country', 'city',
            'inspector_name', 'violation_street_number', 'violation_street_name',
            'violation_zip_code', 'violation_description',
            'mailing_address_str_number', 'mailing_address_str_name',
            'non_us_str_code', 'agency_name', 'state', 'disposition',
            'ticket_issued_date', 'hearing_date', 'grafitti_status', 'violation_code','address']
train_df.drop(string_list,axis=1,inplace=True)
train_df.shape


# In[57]:

test.drop(string_list,axis=1,inplace=True)


# In[58]:

test.columns


# In[59]:

train_df.columns


# In[60]:

train_df.lat.fillna(method = 'ffill',inplace=True)
train_df.lon.fillna(method = 'ffill',inplace=True)
test.lat.fillna(method = 'ffill',inplace=True)
test.lon.fillna(method = 'ffill',inplace=True)
test=test.set_index('ticket_id')
train_df= train_df.set_index('ticket_id')
test


# In[61]:

X_train = train_df[train_df.columns.drop('compliance')]
y_train = train_df['compliance']
X_test = test


# In[62]:

from datetime import datetime
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
model = MLPClassifier()


# In[63]:

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# model = MLPClassifier(hidden_layer_sizes=[100,10],alpha=0.01,random_state=0,
#                      solver='lbfgs',verbose=0)
# model.fit(X_train_scaled,y_train)

# y_proba = model.predict_proba(X_test_scaled)[:,1]

# In[ ]:

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
grid_values = ({'alpha':[0.01],'hidden_layer_sizes':[[100,10],[150,10]]})
grid_model = GridSearchCV(model,param_grid=grid_values,scoring='roc_auc')
grid_model.fit(X_train_scaled,y_train)


# In[ ]:

y_proba = grid_model.predict_proba(X_test_scaled)[:,1]
test_df = pd.read_csv('test.csv',encoding = "ISO-8859-1")
test_df['compliance'] = y_proba
test_df.set_index('ticket_id',inplace=True)


# In[36]:

def blight_model():
    
    return test_df.compliance
blight_model()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



