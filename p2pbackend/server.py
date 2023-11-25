from flask import Flask, jsonify, request
from distributor import Sender
from flask_cors import CORS, cross_origin
import json
from utils import get_active_peers
from userdetails import get_details
from download.download import make_download_requests, request_download


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
    s.upload_file(data['file'], peers)
    dic = {"status": 201, "message": "Uploading file"}
    response = jsonify(dic)
    return response


@app.route("/download/<file_uid>", methods=["GET"])
@cross_origin()
def download_file(file_uid):
    message = make_download_requests(file_uid)
    return "Success"

@app.route("/download/request", methods=["POST"])
@cross_origin()
def request_part():
    data = request.json
    data = json.loads(data)
    request_download(data['file_uid'], data['seeder_info'])
    return "Success"
    


@app.route("/update", methods=["PUT"])
@cross_origin()
def update_peer():
    print("DETAILS")
    user_details = get_details()
    print("oKK")
    print(user_details)
    if not user_details:
        dic = {"status": 404, "message": "USER NOT FOUND"}
        res = jsonify(dic)
        return res
    else:
        dic = {"status": 201, "message": "UPDATED"}
        res = jsonify(dic)
        print("OKKK", res)
        return res
 
if __name__ == "__main__":
    app.run(host="0.0.0.0")
