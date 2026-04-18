from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/api/v2/comprar', methods=['GET', 'POST', 'OPTIONS'])
def realizar_compra():
    # Handle CORS OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    # GET para pruebas rápidas
    if request.method == 'GET':
        return jsonify({
            "mensaje": "Microservicio Flask v2 activo",
            "endpoint": "/api/v2/comprar",
            "metodos": ["GET", "POST"],
            "ejemplo_post": {
                "producto_id": 123,
                "cantidad": 5
            }
        }), 200
    
    # POST para procesar compras reales
    data = None
    
    # Intenta obtener JSON de múltiples formas
    try:
        # Opción 1: get_json()
        data = request.get_json(force=True, silent=True)
    except:
        pass
    
    # Opción 2: Si el body es JSON raw
    if not data and request.data:
        try:
            data = json.loads(request.data)
        except:
            pass
    
    # Opción 3: Intenta form data
    if not data and request.form:
        data = request.form.to_dict()
    
    # Si aún no hay data, devuelve error
    if not data:
        return jsonify({"error": "No se recibió JSON válido en el body"}), 400

    # Simulacion de logica de negocio extraida
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad', 1)

    if not producto_id:
        return jsonify({"error": "Falta el ID del producto"}), 400

    return jsonify({
        "mensaje": "Compra procesada exitosamente por el Microservicio Flask (v2)",
        "producto_id": producto_id,
        "cantidad": cantidad,
        "status": "Aprobado"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
