from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "DevSecOps Telegram Agent Demo App is running",
        "status": "ok"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

if __name__ == "__main__":
    print("Flask starting...")
    app.run(host="0.0.0.0", port=5000)