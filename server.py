from flask import Flask, request, jsonify, render_template
import operaciones

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/suma', methods=['GET'])
def suma():
  a = float(request.args.get('a'))
  b = float(request.args.get('b'))
  return jsonify(result=operaciones.suma(a, b))

@app.route('/resta', methods=['GET'])
def resta():
  a = float(request.args.get('a'))
  b = float(request.args.get('b'))
  return jsonify(result=operaciones.resta(a, b))

@app.route('/multiplicacion', methods=['GET'])
def multiplicacion():
  a = float(request.args.get('a'))
  b = float(request.args.get('b'))
  return jsonify(result=operaciones.multiplicacion(a, b))

@app.route('/division', methods=['GET'])
def division():
  a = float(request.args.get('a'))
  b = float(request.args.get('b'))
  return jsonify(result=operaciones.division(a, b))

if __name__ == '__main__':
  app.run(debug=True)

