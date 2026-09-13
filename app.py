from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Python App! 🚀 CI/CD with Jenkins, Kubernetes and ngrok"

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
