import os 
from flask import Flask, jsonify, send_from_directory, abort
from dotenv import load_dotenv

load_dotenv() # loads env variables

DIST_DIR = os.path.join(os.path.dirname(__file__), "..", "client", "dist")
app = Flask(__name__, static_folder=None)

# API routes
@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.errorhandler(Exception)
def handle_error(e):
    code = getattr(e, "code", 500)
    return jsonify(error=str(e)), code

#  serve react build in production
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path.startswith("api/"):
        abort(404)

    file_path = os.path.join(DIST_DIR, path)
    if path and os.path.exists(file_path):
        return send_from_directory(DIST_DIR, path)

    return send_from_directory(DIST_DIR, "index.html")

if __name__ == "__main__":
    app.run(port=5001, debug=True)