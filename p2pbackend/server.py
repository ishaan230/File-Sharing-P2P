from flask import Flask, jsonify, request
from distributor import Sender
from flask_cors import CORS, cross_origin
import json
from utils import get_active_peers

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=["POST"])
def test():
    print(request.data)
    print("OKK")
    return jsonify({"status": 200, "message": "Hello from torent server"})


@app.route("/upload", methods=["POST"])
@cross_origin()
def upload_file():
    data = request.data.decode('utf-8').replace("'",'"')
    data = json.loads(data)
    peers = get_active_peers()
    print("PEER", peers)
    s = Sender()
    # s.upload_file(data['file'], [('0.0.0.0', 8000)])
    dic = {"status": 201, "message": "Uploading file"}
    response = jsonify(dic)
    return response


@app.route("/download", methods=["POST"])
@cross_origin()
def download_file():
    print(request.data)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
