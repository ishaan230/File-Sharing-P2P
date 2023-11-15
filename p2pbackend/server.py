from flask import Flask, jsonify, request
from distributor import Sender

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_file():
    print(request.data)
    s = Sender()
    s.upload_file(request.data['file_path'], ('0.0.0.0', 8000))
    response = jsonify({"status": 201, "message": "Uploading started"})
    response.status_code = 201
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/download", methods=["POST"])
def download_file():
    print(request.data)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
