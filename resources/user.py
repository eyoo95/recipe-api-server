from http import HTTPStatus
from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class UserRegisterResource(Resource):
    def post(self):
        # {
        #     "username": "홍길동",
        #     "email": "abc@naver.com",
        #     "password": "1234"
        # }

        data = request.get_json()

        # 이메일 주소형식을 확인한다.

        

        return