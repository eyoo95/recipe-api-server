from http import HTTPStatus
from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector
from email-validator import validate_email, EmailNotValidError

class UserRegisterResource(Resource):
    def post(self):
        # {
        #     "username": "홍길동",
        #     "email": "abc@naver.com",
        #     "password": "1234"
        # }

        data = request.get_json()

        # 이메일 주소형식을 확인한다.
        

        email = "my+address@mydomain.tld"

        try:
        # Validate & take the normalized form of the email
        # address for all logic beyond this point (especially
        # before going to a database query where equality
        # does not take into account normalization).
        email = validate_email(email).email
        except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        print(str(e))



        return