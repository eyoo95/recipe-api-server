from flask import Flask, jsonify, request
from http import HTTPStatus

from flask_restful import Api

app = Flask(__name__)

API = Api(app)



if __name__ == '__main__' :
    app.run()