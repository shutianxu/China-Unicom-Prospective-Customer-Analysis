# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:22:48 2018
@author: 1707500
v1.0购车重要因素分析
v1.1增加部分数据处理，用众数，平均值，0取代NAN值
v1.2调整部分参数

V2.0增加用户画像建模
V2.1NAN值改为中位数
V2.2用户画像选取连续值

V3.0增加皮尔逊相关系数分析

V3.1增加主流网站使用情况,统计数据为97W（驻留-APP访问，经销商-app访问-驻留）
V3.2增加其他分类算法比较
V3.3增加RF算法原理解释
V3.4target改为经销商加1月汽车之家,加入访问日表
"""

"""
Random_Forest 算法原理：
1、决策树算法基本原理:通过信息增益，或者GINI指数来划分label属性（信息熵是用来测量样本纯度的指标；信息熵越小，纯度越高）
Ent(D) = -∑ Pk log2 Pk(假定样本合计D中的第K类样本所占的比例为Pk)
Gain(D,a) = Ent(D) - ∑ (|Dv|/|D| Ent(D))  (v为a属性中有V个可能的取值)
Gain(D,a)(信息增益)越大，意味着使用属性a来进行划分所获得的纯度提升越大
连续值采用连续属性离散化处理

与信息增益相反，基尼指数越小则纯度越高，SK-LEARN中默认为基尼指数


2、随机森林原理
bagging做了随机N个样本做基学习器，再将N个基学习器结合
随机森林在bagging的基础上，进一步在决策树的训练中引入了随机选择特征的，d<<总特征数M，一般选择为d = M^0.5,通常相比bagging随机森林的泛化误差更小，而且训练效率更快
随机森林增加了样本扰动和特征扰动来减小泛化误差

"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

header = ['device_number' ,'cust_sex' ,'years_old' ,'yingyongshangdian_dura' ,'tuangoudazhe_dura' ,'shangwubangong_dura' ,'jishitongxun_dura' ,'dacheruanjian_dura' ,'car_owner' ,'area_price' ,'distance' ,'daohang_cnt' ,'daohang_dura' ,'didi_cnt' ,'didi_dura' ,'autohome_cnt' ,'autohome_dura' ,'gongxiangdanche_cnt' ,'gongxiangdanche_dura' ,'autohome_cnt_201712' ,'autohome_dura_201712' ,'autohome_cnt_201711' ,'autohome_dura_201711' ,'gongxiangqiche_cnt' ,'gongxiangqiche_dura' ,'yinyue_cnt' ,'yinyue_dura' ,'zhifubao_cnt' ,'zhifubao_dura' ,'wechat_cnt' ,'wechat_dura' ,'taobao_cnt' ,'taobao_dura' ,'zhihu_cnt' ,'zhihu_dura' ,'meituan_cnt' ,'meituan_dura' ,'mayi_cnt' ,'mayi_dura' ,'foot_distance' ,'bike_distance' ,'car_distance' ,'vis_deal_cnt' ,'xiandai_dealer_cnt' ,'gas_vis_cnt']
data = pd.read_csv("C:/Users/1707500/Desktop/cusc_data_02.csv", sep = '\t',encoding = 'gb2312',names = header)

# =============================================================================
# print(df)
# =============================================================================

data = data.drop(["device_number","didi_cnt","autohome_cnt_201711","gongxiangqiche_cnt","gongxiangqiche_dura","gas_vis_cnt","xiandai_dealer_cnt","daohang_cnt","autohome_cnt"],axis=1)

data = data.drop(["gongxiangdanche_cnt","yinyue_cnt","zhifubao_dura","wechat_cnt","autohome_cnt_201712","taobao_cnt","zhihu_cnt","meituan_dura","mayi_cnt"],axis=1)

data = data.drop(["meituan_cnt"],axis=1)
# =============================================================================
# data = data.dropna(axis=0)
# =============================================================================
# =============================================================================
# print(data.dtypes)
# =============================================================================
# =============================================================================
# data = data.fillna('missing')
# =============================================================================
# =============================================================================
# data = data.fillna(0.00001)
# =============================================================================

data['cust_sex'] = data['cust_sex'].fillna('missing')
data['years_old'] = data['years_old'].fillna('missing')
data['car_owner'] = data['car_owner'].fillna(0)

# =============================================================================
# data['area_price'] = data['area_price'].fillna(data['area_price'].mean())
# data['distance'] = data['distance'].fillna(data['distance'].mean())
# =============================================================================

# =============================================================================
# print(data['area_price'].value_counts())
# print(data['distance'].value_counts())
# =============================================================================


data['area_price'] = data['area_price'].fillna(data['area_price'].median())
data['distance'] = data['distance'].fillna(data['distance'].median())
data['daohang_dura'] = data['daohang_dura'].fillna(0)
data['gongxiangdanche_dura'] = data['gongxiangdanche_dura'].fillna(0)
data['autohome_dura_201712'] = data['autohome_dura_201712'].fillna(0)
data['autohome_dura_201711'] = data['autohome_dura_201711'].fillna(0)
data['autohome_dura'] = data['autohome_dura'].fillna(0)
data['didi_dura'] = data['didi_dura'].fillna(0)

data['yingyongshangdian_dura'] = data['yingyongshangdian_dura'].fillna(0)
data['tuangoudazhe_dura'] = data['tuangoudazhe_dura'].fillna(0)
data['shangwubangong_dura'] = data['shangwubangong_dura'].fillna(0)
data['jishitongxun_dura'] = data['jishitongxun_dura'].fillna(0)
data['dacheruanjian_dura'] = data['dacheruanjian_dura'].fillna(0)
data['yinyue_dura'] = data['yinyue_dura'].fillna(0)





# =============================================================================
# data['zhifubao_cnt'] = data['zhifubao_cnt'].fillna(0)
# data['wechat_dura'] = data['wechat_dura'].fillna(0)
# data['taobao_dura'] = data['taobao_dura'].fillna(0)
# =============================================================================
data['zhihu_dura'] = data['zhihu_dura'].fillna(0)
# =============================================================================
# data['meituan_cnt'] = data['meituan_cnt'].fillna(0)
# =============================================================================
data['mayi_dura'] = data['mayi_dura'].fillna(0)


data['foot_distance'] = data['foot_distance'].fillna(data['foot_distance'].median())
data['car_distance'] = data['car_distance'].fillna(data['car_distance'].median())
data['bike_distance'] = data['bike_distance'].fillna(data['bike_distance'].median())




data['vis_deal_cnt'] = data['vis_deal_cnt'].fillna(0)
data = data.dropna(axis=0)


data['label_1'] = data['vis_deal_cnt'].map(lambda x: 1 if x >= 1 else 0)
data['label_2'] = data['autohome_dura'].map(lambda x: 1 if x >= 1 else 0)

data = data.drop(["vis_deal_cnt"],axis=1)
data = data.drop(["autohome_dura"],axis=1)


data['label'] = (data.label_1) & (data.label_2)
data = data.drop(["label_1"],axis=1)
data = data.drop(["label_2"],axis=1)


# =============================================================================
# null_counts = data.isnull().sum()
# print(null_counts)
# =============================================================================

# =============================================================================
# data.describe()
# =============================================================================

# =============================================================================
# data = data[data.distance < 50000]
# data = data[data.bike_distance < 64000]
# data = data[data.car_distance  < 64000]
# =============================================================================
# =============================================================================
# data = data[data.daohang_dura  < 194000]
# data = data[data.autohome_dura_201712  < 194000]
# data = data[data.autohome_dura_201711  < 194000]
# data = data[data.autohome_dura  < 194000]
# =============================================================================

# =============================================================================
# data['autohome_01-12'] = data['autohome_dura'] - data['autohome_dura_201712']
# data['autohome_12-11'] = data['autohome_dura_201712'] - data['autohome_dura_201711']
# data['autohome_01-11'] = data['autohome_dura'] - data['autohome_dura_201711']
# =============================================================================

orig_columns = data.columns
drop_columns = []
for col in orig_columns:
    col_series = data[col].dropna().unique()
    if len(col_series) == 1:
        drop_columns.append(col)
data = data.drop(drop_columns, axis=1)
print(drop_columns)

# =============================================================================
# data.describe()
# =============================================================================

target = data['label']

# =============================================================================
# null_counts = data.isnull().sum()
# print(null_counts)
# =============================================================================
# =============================================================================
# print(target.value_counts())
# =============================================================================


features = pd.get_dummies(data, columns = ['cust_sex','years_old'])
features = features.drop(['years_old_missing','cust_sex_missing',"label"],axis=1)


# =============================================================================
# from patsy import dmatrices,dmatrix    #凡是分类变量均要使用哑变量处理
# CX = dmatrix ('C(years_old) + C(cust_sex)',data = data ,return_type = 'dataframe')
# XXX=data.drop(["years_old","cust_sex","label"], axis=1)
# features = CX.join(XXX)
# 
# features = features.drop(['C(cust_sex)[T.missing]','C(years_old)[T.missing]'],axis=1)
# # =============================================================================
# # features.describe()
# # =============================================================================
# 
# 
# 
# =============================================================================



##基于树的方法不用做标准化、归一化处理
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
features_new = min_max_scaler.fit_transform(features)
features = pd.DataFrame(features_new, columns=features.columns)




from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report   
from sklearn import metrics


# =============================================================================
# from scipy.stats import pearsonr  
# 
# print( "pearsonr:", pearsonr(features['foot_distance'],features['car_distance']))  
# print( "pearsonr:", pearsonr(features['autohome_dura_201712'],features['autohome_dura_201711']))  
# print( "pearsonr:", pearsonr(features['autohome_dura_201712'],features['autohome_cnt_201712']))  
# =============================================================================






X_train,X_test,y_train,y_test = train_test_split(
features,target,test_size=0.25,random_state=42)

'''
Random_forset 
'''
clf = RandomForestClassifier(n_estimators=50,max_depth = 15,min_samples_split = 250,min_samples_leaf = 25,random_state=42,class_weight="balanced")
clf = clf.fit(X_train, y_train)
y_pre = clf.predict(X_test)

y_pre_pro = clf.predict_proba(X_test)[:, 1]
print(y_pre_pro)
print(classification_report(y_test,y_pre))
print(metrics.roc_auc_score(y_test,y_pre))  #预测Y值得分

def aucfun(act,pred):
    fpr,tpr,thresholds = metrics.roc_curve(act,pred)
    plt.plot(fpr, tpr, color='darkorange',lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
# =============================================================================
#     print(fpr)
#     print(tpr)
#     print(thresholds)
# =============================================================================
    return metrics.auc(fpr,tpr)


aucfun(y_test,y_pre_pro)
# =============================================================================
# num = 1        
# for j in [50,100]:
#     for i in range(100):
#         if ((i%5 == 0) and i != 0):
#             for k in range(2001):
#                 if ((k%200 ==0) and (k != 0)):
#                     print("Index: %d" %num)
#                     print("n_estimators:%d" % j)
#                     print("max_depth:%d" % (i))
#                     print("min_samples_split:%d" % (k))
#                     clf = RandomForestClassifier(n_estimators=j, max_depth=i ,min_samples_split=k, random_state=42,class_weight="balanced")
#                     clf = clf.fit(X_train, y_train) 
#                     y_pre = clf.predict(X_test)
# 
#                     print(classification_report(y_test,y_pre))
#                     print(metrics.roc_auc_score(y_test,y_pre)) #预测Y值得分
#                     
#                     importances = clf.feature_importances_
#                     std = np.std([tree.feature_importances_ for tree in clf.estimators_],axis=0)
#                     indices = np.argsort(importances)[::-1]
#                     # Print the feature ranking
#                     print("Feature ranking:")
#                     for f in range(features.shape[1]):
#                         print("%d. feature %d (%f): %s" % (f + 1, indices[f], importances[indices[f]] , features.columns[indices[f]] ))
# 
#                     with open('D:/document/crawling/random_forest_vis_dealer_v01.txt','a') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！                        
#                         f.write('\n')
#                         f.write('\n')
#                         f.write("Index: %d" %num)
#                         f.write('\n')
#                         f.write("n_estimators:%d" % j)`
#                         f.write('\n')
#                         f.write("max_depth:%d" % (i))
#                         f.write('\n')
#                         f.write("min_samples_split:%d" % (k))
#                         f.write('\n')
#                         f.write(classification_report(y_test,y_pre))                    
#                         f.write(str(metrics.roc_auc_score(y_test,y_pre)))
#                         f.write('\n')
#                         f.write('\n')
#                         f.write('Feature ranking:')
#                         for ll in range(features.shape[1]):
#                             f.write(str("%d. feature %d (%f): %s" % (ll + 1, indices[ll], importances[indices[ll]] , features.columns[indices[ll]] )))
#                             f.write('\n')
#                         f.write('\n')
#                     num = num + 1
# 
# =============================================================================





importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],axis=0)
indices = np.argsort(importances)[::-1]
print("Feature ranking:")
for f in range(features.shape[1]):
    print("%d. feature %d (%f): %s" % (f + 1, indices[f], importances[indices[f]] , features.columns[indices[f]] ))

# =============================================================================
# '''
# LogisticRegression
# '''
# from sklearn.linear_model import LogisticRegression  
# from sklearn.model_selection import train_test_split 
# 
# 
# classifier = LogisticRegression(fit_intercept = True, penalty='l2', C = 1e9,class_weight="balanced")  
# model = classifier.fit(X_train, y_train)               # 训练数据来学习 
# 
# y_pre = model.predict(X_test)
# print(classification_report(y_test,y_pre))  
# print(metrics.roc_auc_score(y_test,y_pre)) #预测Y值得分
# 
# # =============================================================================
# # print(zip(features.columns, np.transpose(model.coef_)))
# # =============================================================================
# 
# indices = np.argsort(model.coef_)[::-1]
# print("Feature ranking:")
# for f in range(features.shape[1]):
#      print("%s. feature %s(%s) : %s" % (f + 1, int(indices[0][f]),model.coef_[0][indices[0][f]],features.columns[int(indices[0][f])]))
# 
#      
# =============================================================================
     
     
# =============================================================================
# '''
# GradientBoosting
# '''
# 
# from sklearn.datasets import make_hastie_10_2
# from sklearn.ensemble import GradientBoostingClassifier
# 
# clf = GradientBoostingClassifier(n_estimators=50,learning_rate=0.1,max_depth = 15 ,min_samples_split = 5000 ,min_samples_leaf = 100, random_state = None , max_features='auto')
# 
# clf = clf.fit(X_train, y_train)
# y_pre = clf.predict(X_test)
# print(classification_report(y_test,y_pre))
# print(metrics.roc_auc_score(y_test,y_pre)) #预测Y值得分
#      
# 
# importances = clf.feature_importances_
# indices = np.argsort(importances)[::-1]
# print("Feature ranking:")
# for f in range(features.shape[1]):
#     print("%d. feature %d (%f): %s" % (f + 1, indices[f], importances[indices[f]] , features.columns[indices[f]] ))
#     
# =============================================================================
    
    



    
