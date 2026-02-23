from flask import Flask, request, jsonify

app = Flask(__name__)

device_registry = {}

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    ip = data.get("ip")
    name = data.get("name")

    device_registry[name] = ip

    print(f"Device registered: {name} at {ip}")

    return jsonify({"status": "registered"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)