from flask import Flask, request, jsonify
import json
import sys

app = Flask(__name__)

@app.route('/api/v2/comprar', methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
def realizar_compra():
    if request.method == 'OPTIONS' or request.method == 'HEAD':
        return '', 204
    
    if request.method == 'GET':
        return jsonify({
            "mensaje": "Microservicio Flask v2 activo"
        }), 200
    
    # POST from any source (curl, Postman, etc)
    data = None
    
    # Read body completely
    body_bytes = request.get_data()
    
    print(f"\nDEBUG REQUEST:", file=sys.stderr)
    print(f"  Method: {request.method}", file=sys.stderr)
    print(f"  Content-Type: {request.content_type}", file=sys.stderr)
    print(f"  Content-Length header: {request.headers.get('Content-Length', 'NONE')}", file=sys.stderr)
    print(f"  Transfer-Encoding: {request.headers.get('Transfer-Encoding', 'NONE')}", file=sys.stderr)
    print(f"  Body bytes length: {len(body_bytes)}", file=sys.stderr)
    print(f"  Body: {body_bytes}", file=sys.stderr)
    
    # Try to parse as JSON
    if body_bytes:
        try:
            body_str = body_bytes.decode('utf-8').strip()
            if body_str:
                data = json.loads(body_str)
                print(f"✓ Parsed JSON: {data}", file=sys.stderr)
        except Exception as e:
            print(f"✗ JSON parse error: {e}", file=sys.stderr)
    
    if not data:
        print(f"✗ NO DATA RECEIVED", file=sys.stderr)
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
