import re
import math
from urllib.parse import urlparse
import pandas as pd

def procesar_url(url):
  parsed_url = urlparse(url)

  netloc = parsed_url.netloc

  # Extract TLD
  tld = netloc.split('.')[-1]

  url_has_login = int("login" in url.lower())
  url_has_client = int("client" in url.lower())
  url_has_server = int("server" in url.lower())
  url_has_admin = int("admin" in url.lower())
  url_has_ip = int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", url)))
  url_isshorted = int(len(url) < 20)
  url_len = len(url)
  url_entropy = calcular_entropia(url)
  url_count_dot = url.count('.')
  url_count_https = url.count('https')
  url_count_http = url.count('http')
  url_count_perc = url.count('%')
  url_count_hyphen = url.count('-')
  url_count_www = url.count('www')
  url_count_atrate = url.count('@')
  url_count_hash = url.count('#')
  url_count_semicolon = url.count(';')
  url_count_underscore = url.count('_')
  url_count_ques = url.count('?')
  url_count_equal = url.count('=')
  url_count_amp = url.count('&')
  url_count_letter = sum(c.isalpha() for c in url)
  url_count_digit = sum(c.isdigit() for c in url)
  sensitive_financial_words = ["bank", "secure", "account", "payment"]
  sensitive_words = ["login", "signin", "admin", "password"]
  url_count_sensitive_financial_words = sum(word in url.lower() for word in sensitive_financial_words)
  url_count_sensitive_words = sum(word in url.lower() for word in sensitive_words)
  url_nunique_chars_ratio = len(set(url)) / len(url)
  path_len = len(parsed_url.path)
  path_count_no_of_dir = parsed_url.path.count('/')
  path_count_no_of_embed = parsed_url.path.count('.')
  path_count_zero = parsed_url.path.count('0')
  path_count_pertwent = parsed_url.path.count('%20')
  path_has_any_sensitive_words = int(any(word in parsed_url.path.lower() for word in sensitive_words))
  path_count_lower = sum(c.islower() for c in parsed_url.path)
  path_count_upper = sum(c.isupper() for c in parsed_url.path)
  path_count_nonascii = sum(c not in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in parsed_url.path)
  path_has_singlechardir = int(any(len(part) == 1 for part in parsed_url.path.split('/')))
  path_has_upperdir = int(any(part.isupper() for part in parsed_url.path.split('/')))
  query_len = len(parsed_url.query)
  query_count_components = parsed_url.query.count('&')
  pdomain = parsed_url.netloc.split('.')
  pdomain_len = len(pdomain)
  pdomain_count_hyphen = parsed_url.netloc.count('-')
  pdomain_count_atrate = parsed_url.netloc.count('@')
  pdomain_count_non_alphanum = sum(not c.isalnum() for c in parsed_url.netloc)
  pdomain_count_digit = sum(c.isdigit() for c in parsed_url.netloc)
  tld = pdomain[-1] if pdomain_len > 1 else ''
  tld_len = len(tld)
  tld_is_sus = int(tld in [
    "xyz", "top", "loan", "win", "club", "click", "support", "men", "party",
    "gq", "cf", "ml", "tk", "work", "biz", "pw", "info", "ru", "cc", "ph"
  ])
  subdomain_len = len(parsed_url.hostname.split('.')[0]) if parsed_url.hostname else 0
  subdomain_count_dot = parsed_url.hostname.count('.') if parsed_url.hostname else 0

  resultado = {
    "url": url,
    "label": 0,
    "url_has_login": url_has_login,
    "url_has_client": url_has_client,
    "url_has_server": url_has_server,
    "url_has_admin": url_has_admin,
    "url_has_ip": url_has_ip,
    "url_isshorted": url_isshorted,
    "url_len": url_len,
    "url_entropy": url_entropy,
    "url_count_dot": url_count_dot,
    "url_count_https": url_count_https,
    "url_count_http": url_count_http,
    "url_count_perc": url_count_perc,
    "url_count_hyphen": url_count_hyphen,
    "url_count_www": url_count_www,
    "url_count_atrate": url_count_atrate,
    "url_count_hash": url_count_hash,
    "url_count_semicolon": url_count_semicolon,
    "url_count_underscore": url_count_underscore,
    "url_count_ques": url_count_ques,
    "url_count_equal": url_count_equal,
    "url_count_amp": url_count_amp,
    "url_count_letter": url_count_letter,
    "url_count_digit": url_count_digit,
    "url_count_sensitive_financial_words": url_count_sensitive_financial_words,
    "url_count_sensitive_words": url_count_sensitive_words,
    "url_nunique_chars_ratio": url_nunique_chars_ratio,
    "path_len": path_len,
    "path_count_no_of_dir": path_count_no_of_dir,
    "path_count_no_of_embed": path_count_no_of_embed,
    "path_count_zero": path_count_zero,
    "path_count_pertwent": path_count_pertwent,
    "path_has_any_sensitive_words": path_has_any_sensitive_words,
    "path_count_lower": path_count_lower,
    "path_count_upper": path_count_upper,
    "path_count_nonascii": path_count_nonascii,
    "path_has_singlechardir": path_has_singlechardir,
    "path_has_upperdir": path_has_upperdir,
    "query_len": query_len,
    "query_count_components": query_count_components,
    "pdomain_len": pdomain_len,
    "pdomain_count_hyphen": pdomain_count_hyphen,
    "pdomain_count_atrate": pdomain_count_atrate,
    "pdomain_count_non_alphanum": pdomain_count_non_alphanum,
    "pdomain_count_digit": pdomain_count_digit,
    "tld_len": tld_len,
    "tld": tld,
    "tld_is_sus": tld_is_sus,
    "subdomain_len": subdomain_len,
    "subdomain_count_dot": subdomain_count_dot,
  }

  cargar_y_actualizar_dataset(resultado)
  return resultado

def cargar_y_actualizar_dataset(url_data, csv_path="train_dataset2.csv"):
  try:
    # Load existing dataset
    dataset = pd.read_csv(csv_path)
    print(f"Archivo CSV '{csv_path}' cargado correctamente.")
  except FileNotFoundError:
    # If file doesn't exist, create a new DataFrame
    dataset = pd.DataFrame(columns=url_data.keys())
    print(f"Archivo CSV '{csv_path}' no encontrado. Se creará un nuevo archivo.")

  # Append new data
  dataset = dataset._append(url_data, ignore_index=True)

  # Save updated dataset back to CSV
  dataset.to_csv(csv_path, index=False)
  print(f"Nuevos datos guardados correctamente en '{csv_path}'.")

def calcular_entropia(s):
  probabilities = [float(s.count(c)) / len(s) for c in set(s)]
  return -sum(p * math.log(p) / math.log(2.0) for p in probabilities)

# url_examples = [
#   "https://www.bank-secure-login.com",
#   "http://123.456.789.000",
#   "https://client-server.example.com/admin",
#   "http://short.co",
#   "https://example.com/path/to/resource?query=1&another=2",
#   "https://example-site.com/login",
#   "http://example-with-dashes.com",
#   "https://secure-payment.example.com",
#   "http://example.com/path/with%20spaces",
#   "https://example.com/path/to/file_with_underscores",
#   "http://example.com/path/with@sign",
#   "https://www.example.com/path/to/server123",
#   "http://example.com/path/to/resource;param",
#   "https://example.com/path/to?query#hash",
#   "http://example.com/path/to/resource=equals",
#   "http://example.com/path/to?query&another=amp",
#   "http://example.com/short-path",
#   "https://example.com/admin/login",
#   "http://example.com/path/with%20percent",
#   "https://www.example.com/very/long/path/with/many/directories",
#   "https://www.example-with-sus.xyz",
#   "http://example.com/path/to/financial-info",
# ]

# for url in url_examples:
#   resultado = procesar_url(url)
#   print(resultado)