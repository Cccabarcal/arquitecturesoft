from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/v2/comprar', methods=['POST'])
def comprar():
    """
    Endpoint del microservicio Flask para procesar pagos.
    Este es el nuevo servicio que estrangula la funcionalidad de compra del monolito.
    """
    try:
        data = request.get_json()
        
        # Validar datos básicos
        if not data:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Cuerpo de la solicitud vacío'
            }), 400
        
        # Procesar el pago (lógica simplificada para demostración)
        respuesta = {
            'estado': 'procesada exitosamente por el Microservicio Flask',
            'timestamp': datetime.now().isoformat(),
            'datos_recibidos': data,
            'servicio': 'Flask Microservicio Pagos (v2)'
        }
        
        return jsonify(respuesta), 200
    
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Flask Microservicio Pagos'
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Endpoint raíz"""
    return jsonify({
        'mensaje': 'Microservicio Flask para Pagos',
        'versión': '2.0',
        'endpoints': [
            '/api/v2/comprar (POST)',
            '/health (GET)'
        ]
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
