from flask import Flask, request, jsonify
import json
import sys

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
    
    # POST - Debug completo
    print("\n" + "="*50, file=sys.stderr)
    print(f"REQUEST HEADERS: {dict(request.headers)}", file=sys.stderr)
    print(f"REQUEST CONTENT_LENGTH: {request.content_length}", file=sys.stderr)
    print(f"REQUEST DATA (bytes): {request.data}", file=sys.stderr)
    print(f"REQUEST DATA (len): {len(request.data) if request.data else 0}", file=sys.stderr)
    print("="*50, file=sys.stderr)
    
    data = None
    
    # SIEMPRE intenta parsear el body como JSON
    if request.data and len(request.data) > 0:
        try:
            body_str = request.data.decode('utf-8').strip()
            print(f"DECODED BODY: {body_str}", file=sys.stderr)
            if body_str:
                data = json.loads(body_str)
                print(f"✓ PARSED JSON: {data}", file=sys.stderr)
        except Exception as e:
            print(f"✗ ERROR PARSING: {e}", file=sys.stderr)
    else:
        print(f"✗ NO DATA IN REQUEST", file=sys.stderr)
    
    # Si aún no hay data
    if not data:
        return jsonify({"error": "No se recibió JSON válido"}), 400

    # Validar datos
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad', 1)

    if not producto_id:
        return jsonify({"error": "Falta el ID del producto"}), 400

    # Respuesta exitosa
    return jsonify({
        "mensaje": "Compra procesada exitosamente por el Microservicio Flask (v2)",
        "producto_id": producto_id,
        "cantidad": cantidad,
        "status": "Aprobado"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
