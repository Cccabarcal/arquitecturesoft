from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/v2/comprar', methods=['GET', 'POST'])
def realizar_compra():
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
    try:
        # Force parsing JSON desde el request
        data = request.get_json(force=True)
    except:
        # Si no es JSON, intenta desde el body raw
        data = request.form.to_dict()
        if not data:
            return jsonify({"error": "Debes enviar JSON en el body"}), 400

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
    app.run(host='0.0.0.0', port=5000, debug=True)
