import re
import math
from urllib.parse import urlparse

def procesar_url(url):
  parsed_url = urlparse(url)

  url_len = len(url)
  url_entropy = calcular_entropia(url)
  url_count_dot = url.count('.')
  url_count_hyphen = url.count('-')
  url_count_www = url.count('www')
  url_count_atrate = url.count('@')
  url_count_hash = url.count('#')
  url_count_ques = url.count('?')
  url_count_equal = url.count('=')
  url_count_amp = url.count('&')
  url_count_letter = sum(c.isalpha() for c in url)
  url_count_digit = sum(c.isdigit() for c in url)
  path_len = len(parsed_url.path)
  path_count_no_of_dir = parsed_url.path.count('/')
  tld = parsed_url.netloc.split('.')[-1]
  tld_len = len(tld)

  resultado = {
    "url": url,
    "url_len": url_len,
    "url_entropy": url_entropy,
    "url_count_dot": url_count_dot,
    "url_count_hyphen": url_count_hyphen,
    "url_count_www": url_count_www,
    "url_count_atrate": url_count_atrate,
    "url_count_hash": url_count_hash,
    "url_count_ques": url_count_ques,
    "url_count_equal": url_count_equal,
    "url_count_amp": url_count_amp,
    "url_count_letter": url_count_letter,
    "url_count_digit": url_count_digit,
    "path_len": path_len,
    "path_count_no_of_dir": path_count_no_of_dir,
    "tld": tld,
    "tld_len": tld_len,
  }

  return resultado

def calcular_entropia(s):
  probabilities = [float(s.count(c)) / len(s) for c in set(s)]
  return -sum(p * math.log(p) / math.log(2.0) for p in probabilities)
