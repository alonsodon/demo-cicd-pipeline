import time
from flask import Flask, jsonify

app = Flask(__name__)
START_TIME = time.time()


@app.route("/health")
def health():
    """Health check endpoint — requerido por Docker HEALTHCHECK, K8s, load balancers."""
    return jsonify(
        {"status": "ok", "uptime_seconds": round(time.time() - START_TIME, 2)}
    )


@app.route("/greet/<name>")
def greet(name: str):
    """Saluda a alguien."""
    return jsonify({"message": f"Hello, {name}!", "name": name})


@app.route("/echo", methods=["POST"])
def echo():
    """Devuelve el mismo JSON que recibe."""
    from flask import request

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "request body must be JSON"}), 400
    return jsonify({"echo": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
