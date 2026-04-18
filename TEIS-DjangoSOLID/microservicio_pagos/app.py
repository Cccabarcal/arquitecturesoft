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
            "endpoint": "/api/v2/comprar"
        }), 200
    
    # DEBUG: Ver exactamente qué recibe Flask
    print(f"\n=== DEBUG POST ===")
    print(f"Content-Type: {request.content_type}")
    print(f"is_json: {request.is_json}")
    print(f"data (raw): {request.data}")
    print(f"data (decoded): {request.data.decode('utf-8') if request.data else 'EMPTY'}")
    
    data = None
    
    # Opción 1: Si es JSON puro en el body (sin Content-Type)
    if request.data:
        try:
            data = json.loads(request.data.decode('utf-8'))
            print(f"✓ Parsed from request.data")
        except Exception as e:
            print(f"✗ Error parsing request.data: {e}")
    
    # Opción 2: Si tiene Content-Type: application/json
    if not data and request.is_json:
        try:
            data = request.get_json(force=True)
            print(f"✓ Parsed from get_json()")
        except Exception as e:
            print(f"✗ Error in get_json(): {e}")
    
    if not data:
        print(f"✗ No data found!")
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
