from flask import Flask, request, jsonify
import json

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
    print(f"REQUEST METHOD: {request.method}")
    print(f"REQUEST HEADERS: {dict(request.headers)}")
    print(f"REQUEST CONTENT_TYPE: {request.content_type}")
    print(f"REQUEST DATA: {request.data}")
    print(f"REQUEST GET_JSON: {request.get_json(silent=True)}")
    
    data = None
    
    # Intenta obtener JSON
    if request.is_json:
        data = request.get_json()
    elif request.data:
        try:
            data = json.loads(request.data.decode('utf-8'))
        except:
            pass
    
    if not data:
        return jsonify({"error": "No se recibió JSON válido", "debug": "Revisa los logs del servidor"}), 400

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
    app.run(host='0.0.0.0', port=5000)
