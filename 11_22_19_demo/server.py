from flask import Flask
from flask import send_from_directory
app = Flask(__name__)

@app.route('/.well-known/<path:filename>')
def wellKnownRoute(filename):
    return send_from_directory(app.root_path + '/.well-known/', filename, conditional=True)

@app.route("/")
def main():
    return "Hola Mundo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
