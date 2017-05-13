__author__ = 'arpitgarg'

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sys
import json

app = Flask(__name__, static_url_path='')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/topics", methods=['GET', 'POST'])
def topics():
    print "In Server "+request.stream.read()
    f = open('dummy1.json', 'r')
    data = json.load(f)
    print type(data)
    data = json.dumps(data)
    f.close()
    print type(data)
    # return app.send_static_file('dummy.json')
    return data


@app.route("/temporalStrength", methods=['GET', 'POST'])
def temporalStrength():
    print "In Server temporal strength"
    f = open('topicTemporalStrength.json', 'r')
    data = json.load(f)
    print type(data)
    f.close()
    return jsonify(data)
    # data = request.stream.read()


@app.route("/relevantData", methods=['GET', 'POST'])
def relevantData():
    print "In Server relevant"
    f = open('topicRelevantDocuments.json', 'r')
    data = json.load(f)
    print type(data)
    f.close()
    return jsonify(data)
    # data = request.stream.read()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
