from flask import Flask, request, jsonify

app = Flask(__name__)

def sumar(a, b):
    """Función para sumar dos números"""
    try:
        return float(a) + float(b)
    except (ValueError, TypeError):
        raise ValueError("Los valores deben ser números válidos")

def restar(a, b):
    """Función para restar dos números"""
    try:
        return float(a) - float(b)
    except (ValueError, TypeError):
        raise ValueError("Los valores deben ser números válidos")

def multiplicar(a, b):
    """Función para multiplicar dos números"""
    try:
        return float(a) * float(b)
    except (ValueError, TypeError):
        raise ValueError("Los valores deben ser números válidos")

def dividir(a, b):
    """Función para dividir dos números"""
    try:
        num_a = float(a)
        num_b = float(b)
        if num_b == 0:
            raise ValueError("No se puede dividir por cero")
        return num_a / num_b
    except (ValueError, TypeError):
        raise ValueError("Los valores deben ser números válidos")

# Mapa de operaciones disponibles
operaciones = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir
}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculadora Monolítica</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 500px;
                text-align: center;
            }
            
            h1 {
                color: #333;
                margin-bottom: 30px;
                font-size: 2.5em;
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .input-group {
                margin-bottom: 20px;
                text-align: left;
            }
            
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: 600;
                color: #555;
            }
            
            input, select {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }
            
            button {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 8px;
                cursor: pointer;
                transition: transform 0.2s ease;
                width: 100%;
                margin-top: 20px;
            }
            
            button:hover {
                transform: translateY(-2px);
            }
            
            button:active {
                transform: translateY(0);
            }
            
            .resultado {
                margin-top: 30px;
                padding: 20px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                min-height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .resultado.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .resultado.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .loading {
                display: none;
                margin-top: 20px;
            }
            
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧮 Calculadora</h1>
            
            <form id="calculadoraForm">
                <div class="input-group">
                    <label for="numero1">Primer número:</label>
                    <input type="number" id="numero1" step="any" required>
                </div>
                
                <div class="input-group">
                    <label for="operacion">Operación:</label>
                    <select id="operacion" required>
                        <option value="">Selecciona una operación</option>
                        <option value="sumar">➕ Sumar</option>
                        <option value="restar">➖ Restar</option>
                        <option value="multiplicar">✖️ Multiplicar</option>
                        <option value="dividir">➗ Dividir</option>
                    </select>
                </div>
                
                <div class="input-group">
                    <label for="numero2">Segundo número:</label>
                    <input type="number" id="numero2" step="any" required>
                </div>
                
                <button type="submit">Calcular</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Calculando...</p>
            </div>
            
            <div id="resultado" class="resultado" style="display: none;"></div>
        </div>
        
        <script>
            document.getElementById('calculadoraForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const numero1 = document.getElementById('numero1').value;
                const numero2 = document.getElementById('numero2').value;
                const operacion = document.getElementById('operacion').value;
                const resultadoDiv = document.getElementById('resultado');
                const loadingDiv = document.getElementById('loading');
                
                // Mostrar loading
                loadingDiv.style.display = 'block';
                resultadoDiv.style.display = 'none';
                
                try {
                    const response = await fetch(`/calcular?op=${operacion}&a=${numero1}&b=${numero2}`);
                    const data = await response.json();
                    
                    // Ocultar loading
                    loadingDiv.style.display = 'none';
                    resultadoDiv.style.display = 'block';
                    
                    if (response.ok) {
                        resultadoDiv.className = 'resultado success';
                        resultadoDiv.innerHTML = `
                            <div>
                                <strong>Resultado:</strong><br>
                                ${numero1} ${getOperacionSymbol(operacion)} ${numero2} = ${data.resultado}
                            </div>
                        `;
                    } else {
                        resultadoDiv.className = 'resultado error';
                        resultadoDiv.innerHTML = `
                            <div>
                                <strong>Error:</strong><br>
                                ${data.error}
                            </div>
                        `;
                    }
                } catch (error) {
                    loadingDiv.style.display = 'none';
                    resultadoDiv.style.display = 'block';
                    resultadoDiv.className = 'resultado error';
                    resultadoDiv.innerHTML = `
                        <div>
                            <strong>Error de conexión:</strong><br>
                            No se pudo conectar con el servidor
                        </div>
                    `;
                }
            });
            
            function getOperacionSymbol(operacion) {
                const symbols = {
                    'sumar': '+',
                    'restar': '-',
                    'multiplicar': '×',
                    'dividir': '÷'
                };
                return symbols[operacion] || operacion;
            }
        </script>
    </body>
    </html>
    '''

@app.route('/calcular', methods=['GET'])
def calcular():
    operacion = request.args.get('op')
    a = request.args.get('a')
    b = request.args.get('b')

    # Validar que se proporcionaron todos los parámetros
    if not operacion or a is None or b is None:
        return jsonify({'error': 'Faltan parámetros: op, a, b son requeridos'}), 400

    # Validar que la operación existe
    if operacion not in operaciones:
        return jsonify({'error': 'Operación no válida. Operaciones disponibles: sumar, restar, multiplicar, dividir'}), 400

    try:
        # Ejecutar la operación
        resultado = operaciones[operacion](a, b)
        return jsonify({'resultado': resultado}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

# Rutas individuales para cada operación (opcional, para compatibilidad)
@app.route('/suma', methods=['GET'])
def suma():
    a = request.args.get('a')
    b = request.args.get('b')
    
    if a is None or b is None:
        return jsonify({'error': 'Parámetros a y b son requeridos'}), 400
    
    try:
        resultado = sumar(a, b)
        return jsonify({'resultado': resultado}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/resta', methods=['GET'])
def resta():
    a = request.args.get('a')
    b = request.args.get('b')
    
    if a is None or b is None:
        return jsonify({'error': 'Parámetros a y b son requeridos'}), 400
    
    try:
        resultado = restar(a, b)
        return jsonify({'resultado': resultado}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/multiplicacion', methods=['GET'])
def multiplicacion():
    a = request.args.get('a')
    b = request.args.get('b')
    
    if a is None or b is None:
        return jsonify({'error': 'Parámetros a y b son requeridos'}), 400
    
    try:
        resultado = multiplicar(a, b)
        return jsonify({'resultado': resultado}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/division', methods=['GET'])
def division():
    a = request.args.get('a')
    b = request.args.get('b')
    
    if a is None or b is None:
        return jsonify({'error': 'Parámetros a y b son requeridos'}), 400
    
    try:
        resultado = dividir(a, b)
        return jsonify({'resultado': resultado}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)