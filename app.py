from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SERVICIOS = {
    "sumar": "https://suma-service.azurewebsites.net/sumar",
    "restar": "https://resta-service.azurewebsites.net/restar",
    "multiplicar": "https://multiplicacion-service.azurewebsites.net/multiplicar",
    "dividir": "https://division-service.azurewebsites.net/dividir"
}

@app.route('/calcular', methods=['GET'])
def calcular():
    op = request.args.get('op')
    a = request.args.get('a')
    b = request.args.get('b')

    if not op or not a or not b:
        return jsonify({"error": "Faltan parámetros: op, a, b"}), 400

    if op not in SERVICIOS:
        return jsonify({"error": f"Operación no válida: {op}"}), 400

    try:
        r = requests.get(SERVICIOS[op], params={"a": a, "b": b})
        return jsonify(r.json()), r.status_code
    except Exception:
        return jsonify({"error": f"No se pudo contactar al servicio de {op}"}), 500

if __name__ == '__main__':
    app.run(port=5000)
