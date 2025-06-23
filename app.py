from flask import Flask, request, jsonify

app = Flask(__name__)

def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b

@app.route('/calcular', methods=['GET'])
def calcular():
    op = request.args.get('op')
    a = request.args.get('a')
    b = request.args.get('b')

    if not op or a is None or b is None:
        return jsonify({"error": "Faltan parámetros: op, a, b"}), 400

    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return jsonify({"error": "Los parámetros a y b deben ser números"}), 400

    operaciones = {
        "sumar": sumar,
        "restar": restar,
        "multiplicar": multiplicar,
        "dividir": dividir
    }

    if op not in operaciones:
        return jsonify({"error": f"Operación no válida: {op}"}), 400

    try:
        resultado = operaciones[op](a, b)
        return jsonify({"resultado": resultado}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
