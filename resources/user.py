from http import HTTPStatus
from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector
from email_validator import validate_email, EmailNotValidError
from utills import hash_password


class UserRegisterResource(Resource):
    def post(self):
        data = request.get_json()

        # 이메일 주소형식을 확인한다.

        try:            
            validate_email(data['email'])

        except EmailNotValidError as e:
            print(str(e))
            return {'error' : str(e)} , 400

        # 비밀번호 암호화
        # 비밀번호의 길이가 유효한지 체크한다. 4자리이상 12자리이상
        if len(data['password']) < 4 or len(data['password'])>12:
            return{'error': '비밀번호 길이는 4자리 이상 12자리 이하이어야 합니다.'}, 400

        hashed_password = hash_password(data['password'])

        # 데이터베이스에 회원정보를 저장한다.

        try :

            # 데이터 insert 
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into user
                    (username, email, password)
                    values
                    (%s, %s, %s);'''

            record = (data['username'], data['email'], hashed_password ) # 튜플형식
            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record )

            # 5. 커넥션을 커밋해줘야 한다 => 디비에 영구적으로 반영하라는 뜻
            connection.commit()

            # DB에 저장된 ID값 가져오기
            user_id = cursor.lastrowid

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error":str(e)}, 503   # 

        return {"result":"success" , "user_id" : user_id}, 200




        return