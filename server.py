from flask import Flask, request, render_template
import conversion  # Asegúrate de que este módulo exista y tenga la función entrenamiento

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
  url = request.form['url']
  print(f'URL recibida: {url}')
  # Llama a la función de conversión y obtén los resultados
  resultado = conversion.entrenamiento(url)
  print(f'Detalles de la URL: {resultado}')
  # return f'<h2>URL recibida: {url}</h2><pre>{resultado}</pre>'
  return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Resultado de la Búsqueda</title></head><body><h1>Resultado de la Búsqueda</h1><h2>URL recibida: { url }</h2><pre>{ resultado }</pre><a href="/">Volver</a></body></html>'
  # return render_template('resultado.html', url=url, resultado=resultado)

if __name__ == '__main__':
  app.run(debug=True)