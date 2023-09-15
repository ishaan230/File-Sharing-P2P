from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_file():
    print(request.data)
    response = jsonify({"status": 201, "message": "Uploading started"})
    response.status_code = 201
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
