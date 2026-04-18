from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/v2/comprar', methods=['GET', 'POST', 'OPTIONS'])
def realizar_compra():
    if request.method == 'OPTIONS':
        return '', 204
    
    if request.method == 'GET':
        return jsonify({
            "mensaje": "Microservicio Flask v2 activo",
            "endpoint": "/api/v2/comprar",
            "metodos": ["GET", "POST"],
            "ejemplo_post": {"producto_id": 123, "cantidad": 5}
        }), 200
    
    # POST - Recibir JSON de CUALQUIER forma
    data = None
    
    # Intento 1: request.is_json
    if request.is_json:
        data = request.get_json(silent=True)
    
    # Intento 2: request.data (raw JSON en el body)
    if not data and request.data:
        try:
            data = json.loads(request.data)
        except:
            pass
    
    # Intento 3: request.form
    if not data and request.form:
        data = request.form.to_dict()
    
    # Si no hay data, error
    if not data:
        return jsonify({"error": "No se recibió JSON válido"}), 400

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
