# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from urllib.parse import urlparse
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score
import numpy as np # linear algebra
from wordcloud import WordCloud
from googlesearch import search


import pandas as pd

# Usar barras diagonales en la ruta
ruta_del_archivo = 'C:/Users/Emanuel/Desktop/malicious_phish.csv'

# Cargar el archivo CSV en un DataFrame
data = pd.read_csv(ruta_del_archivo)

# Mostrar las primeras filas del DataFrame
print(data.head(10))

data.shape
data.type.unique()


phishing_URLs = data[data.type == 'phishing']
Benign_URLs = data[data.type == 'benign']
Defacement_URLs = data[data.type == 'defacement']
Malware_URLs = data[data.type == 'malware']

phishing_URLs

phish = " ".join(i for i in phishing_URLs.url)
wordcloud = WordCloud(width=1600, height=800,colormap='Paired').generate(phish)
plt.figure( figsize=(12,14),facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()


phish = " ".join(i for i in phishing_URLs.url)
wordcloud = WordCloud(width=1600, height=800,colormap='Paired').generate(phish)
plt.figure( figsize=(12,14),facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()



benign= " ".join(i for i in Benign_URLs.url)
wordcloud = WordCloud(width=1600, height=800,colormap='Paired').generate(benign)
plt.figure( figsize=(12,14),facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()


defacement= " ".join(i for i in Defacement_URLs.url)
wordcloud = WordCloud(width=1600, height=800,colormap='Paired').generate(defacement)
plt.figure( figsize=(12,14),facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()


malware= " ".join(i for i in Malware_URLs.url)
wordcloud = WordCloud(width=1600, height=800,colormap='Paired').generate(malware)
plt.figure( figsize=(12,14),facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()


##############################################################################



def having_ip(url):
  try:
    ipaddress.ip_address(url)
    ip = 1
  except:
    ip = 0
  return ip

# The phishing or malware websites generally use more than two sub-domains in the URL.
# Each domain is separated by dot (.). If any URL contains more than three dots(.),
# then it increases the probability of a malicious site.

def count_dot(url):
    count_dot =url.count('.')
    return count_dot

# count @ in url
def AtSign(url):
    return url.count('@')


# check if the URL is indexed in google search console or not

def google_index(url):
    site = search(url, 10)
    return 1 if site else 0

# Count_dir: The presence of multiple directories
#     in the URL generally indicates suspicious websites.

def no_director(url):
    urldir = urlparse(url).path
    return urldir.count('/')

def no_embed_domain(url):
    urldir = urlparse(url).path
    return urldir.count('//')


def num_digits(url):
    dig = [x for x in url if x.isdigit()]
    return len(dig)


def len_url(url):
    return len(url)

def num_parameter(url):
    parameter = url.split('&')
    return len(parameter) - 1

def num_fragments(url):
    fragment = url.split('#')
    return len(fragment) - 1


################################################################################



def feature_extraction(url):

  features = []
  #Address bar based features (10)
  features.append(having_ip(url))
  features.append(count_dot(url))
  features.append(AtSign(url))
  #features.append(h_hostname(url))
  features.append(google_index(url))
  features.append(no_director(url))
  features.append(no_embed_domain(url))
  features.append(num_digits(url))
  features.append(num_parameter(url))
  features.append(num_fragments(url))
  features.append(len_url(url))
  return features


###############################################################################

features_extracted_d = []

for i in range(len(data)):
  url = data.url[i]
  features_extracted_d.append(feature_extraction(url))
  
  ############################################################################
  
  
  features_extracted_d
  
##############################################################################


#converting the list to dataframe
feature_names = ['having_ip', 'count_dot', 'AtSign', 'google_index','no_director','no_embed_domain', 'num_digits',  'num_parameter','num_fragments','len_url']
df = pd.DataFrame(features_extracted_d, columns= feature_names)
df

#############################################################################
final_data = pd.concat([data,df],axis = 1)
#############################################################################

final_data


#############################################################################

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
final_data["target"] = le.fit_transform(final_data["type"])
final_data["target"].value_counts()

#############################################################################

X = final_data.drop(['url','type','target'] , axis = 1)
y = final_data.target

#############################################################################
y
##############################################################################


X_train, X_test, y_train, y_test = train_test_split(X, y,  test_size=0.2,shuffle=True, random_state=0)


###############################################################################

# Importar librerías necesarias
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Suponiendo que ya tienes tus datos de entrenamiento y prueba en X_train, y_train, X_test, y_test

# Entrenar el modelo Random Forest
rf = RandomForestClassifier(n_estimators=100, max_features='sqrt')
rf.fit(X_train, y_train)

# Realizar predicciones
y_pred_rf = rf.predict(X_test)

# Imprimir el informe de clasificación
print(classification_report(y_test, y_pred_rf))

# Calcular y mostrar la precisión
acc = accuracy_score(y_test, y_pred_rf)
print("accuracy:   %0.3f" % acc)



def predict_url(url):
    features = feature_extraction(url)
    prediction = rf.predict([features])[0]
    type_label = le.inverse_transform([prediction])[0]
    if type_label == 'benign':
        return f"La URL '{url}' no es maliciosa."
    else:
        return f"La URL '{url}' es maliciosa y categorizada como {type_label}."

# Example of how to use predict_url
new_url = input("Ingresa URL: ")
result = predict_url(new_url)
print(result)