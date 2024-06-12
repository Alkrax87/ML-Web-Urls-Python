import math
from urllib.parse import urlparse
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
from googlesearch import search
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def entrenamiento(url_input):
  ruta_del_archivo = 'malicious_phish.csv'

  # Cargar el archivo CSV en un DataFrame
  try:
    data = pd.read_csv(ruta_del_archivo)
    print(f"Archivo CSV '{ruta_del_archivo}' cargado correctamente.")
  except FileNotFoundError:
    print(f"Archivo CSV '{ruta_del_archivo}' no encontrado.")
    return

  # Mostrar las primeras filas del DataFrame
  print(data.head(10))

  phishing_URLs = data[data.type == 'phishing']
  Benign_URLs = data[data.type == 'benign']
  Defacement_URLs = data[data.type == 'defacement']
  Malware_URLs = data[data.type == 'malware']

  def having_ip(url):
    try:
      ipaddress.ip_address(url)
      ip = 1
    except:
      ip = 0
    return ip

  def count_dot(url):
    return url.count('.')

  def AtSign(url):
    return url.count('@')

  def google_index(url):
    site = search(url, 10)
    return 1 if site else 0

  def no_director(url):
    urldir = urlparse(url).path
    return urldir.count('/')

  def no_embed_domain(url):
    urldir = urlparse(url).path
    return urldir.count('//')

  def num_digits(url):
    return len([x for x in url if x.isdigit()])

  def len_url(url):
    return len(url)

  def num_parameter(url):
    return len(url.split('&')) - 1

  def num_fragments(url):
    return len(url.split('#')) - 1

  def feature_extraction(url):
    features = []
    features.append(having_ip(url))
    features.append(count_dot(url))
    features.append(AtSign(url))
    features.append(google_index(url))
    features.append(no_director(url))
    features.append(no_embed_domain(url))
    features.append(num_digits(url))
    features.append(num_parameter(url))
    features.append(num_fragments(url))
    features.append(len_url(url))
    return features

  features_extracted_d = [feature_extraction(data.url[i]) for i in range(len(data))]

  feature_names = ['having_ip', 'count_dot', 'AtSign', 'google_index', 'no_director', 'no_embed_domain', 'num_digits', 'num_parameter', 'num_fragments', 'len_url']
  df = pd.DataFrame(features_extracted_d, columns=feature_names)
  final_data = pd.concat([data, df], axis=1)

  le = LabelEncoder()
  final_data["target"] = le.fit_transform(final_data["type"])

  X = final_data.drop(['url', 'type', 'target'], axis=1)
  y = final_data.target

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=0)

  rf = RandomForestClassifier(n_estimators=100, max_features='sqrt')
  rf.fit(X_train, y_train)

  y_pred_rf = rf.predict(X_test)
  print(classification_report(y_test, y_pred_rf))
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

  # Predicción para la URL ingresada
  result = predict_url(url_input)
  print(result)
  return result

def cargar_y_actualizar_dataset(url_data, csv_path="malicious_phish.csv"):
  try:
    dataset = pd.read_csv(csv_path)
    print(f"Archivo CSV '{csv_path}' cargado correctamente.")
  except FileNotFoundError:
    dataset = pd.DataFrame(columns=url_data.keys())
    print(f"Archivo CSV '{csv_path}' no encontrado. Se creará un nuevo archivo.")

  dataset = dataset._append(url_data, ignore_index=True)
  dataset.to_csv(csv_path, index=False)
  print(f"Nuevos datos guardados correctamente en '{csv_path}'.")
