from flask import Flask, request, render_template
import conversion

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
  url = request.form['url']
  print(f'URL recibida: {url}')
  # Llama a la función de conversión y obtén los resultados
  resultado = conversion.procesar_url(url)
  print(f'Detalles de la URL: {resultado}')
  return f'<h2>URL recibida: {url}</h2><pre>{resultado}</pre>'

if __name__ == '__main__':
  app.run(debug=True)