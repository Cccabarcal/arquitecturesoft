from flask import Flask, request, jsonify
import json
import sys

app = Flask(__name__)

@app.route('/api/v2/comprar', methods=['GET', 'POST', 'OPTIONS', 'HEAD'])
def realizar_compra():
    if request.method in ['OPTIONS', 'HEAD']:
        return '', 204
    
    if request.method == 'GET':
        return jsonify({"mensaje": "Microservicio Flask v2 activo"}), 200
    
    # POST - Recibir body de cualquier forma
    data = None
    
    # Obtener el body completo sin importar cómo se envíe
    body_bytes = b''
    try:
        # Lee el stream completamente
        body_bytes = request.stream.read()
    except:
        pass
    
    # Si no funciona stream, intenta get_data
    if not body_bytes:
        body_bytes = request.get_data()
    
    print(f"\nDEBUG POST REQUEST:", file=sys.stderr)
    print(f"  Content-Type: {request.content_type}", file=sys.stderr)
    print(f"  Content-Length: {request.headers.get('Content-Length', 'NONE')}", file=sys.stderr)
    print(f"  Transfer-Encoding: {request.headers.get('Transfer-Encoding', 'NONE')}", file=sys.stderr)
    print(f"  Body bytes (len={len(body_bytes)}): {body_bytes}", file=sys.stderr)
    
    # Intentar parseear como JSON
    if body_bytes:
        try:
            body_str = body_bytes.decode('utf-8').strip()
            print(f"  Decoded: {body_str}", file=sys.stderr)
            if body_str:
                data = json.loads(body_str)
                print(f"  ✓ JSON parsed: {data}", file=sys.stderr)
        except Exception as e:
            print(f"  ✗ Error: {e}", file=sys.stderr)
    else:
        print(f"  ✗ Body is empty!", file=sys.stderr)
    
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
