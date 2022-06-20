from http import HTTPStatus
from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector
from email_validator import validate_email, EmailNotValidError
from utils import hash_password, check_password


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

class UserLoginResource(Resource):
    def post(self):
        # 클라이언트로부터 body로 넘어온 데이터를 받는다.
        data = request.get_json()

        # {
        #     "email": "abc@naver.com",
        #     "password": "123456"
        # }
        try:
            connection = get_connection()
            # 이메일로 DB의 데이터를 가져온다.
            query = '''select * from user
                        where email = %s;'''

            record = (data['email'],  )

            cursor = connection.cursor(dictionary = True)  # 데이터를 셀렉할때 키벨류로 가져온다.

            cursor.execute(query, record )

            # select문은 아래 함수를 이용해서 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)
            
            # 중요! DB 에서 가져온 timestamp는 파이썬의 datetime으로 자동 변경된다.
            # 문제는 이 데이터를 json.으로 바로 보낼수 없으므로 문자열로 바꿔서 다시 저장해서 보낸다.

            i = 0
            for record in result_list:
                result_list[i]['created_at'] = record['created_at'].isoformat()
                result_list[i]['updated_at'] = record['updated_at'].isoformat()
                i = i + 1

            

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error":str(e)}, 503

        # result_list의 행의갯수가 1개면 유저데이터를 받아온것이고 0 이면 등록되지 않은 회원
        if len(result_list) != 1:
            return {'error':'해당되는 이메일 정보가 없습니다.'}, 400

        # 비밀번호가 맞는지 확인
        user_info = result_list[0]
        check = check_password(data['password'],user_info['password'])
        if check == False:
            return {'error':'비밀번호가 맞지 않습니다.'}, 400
        
        return {'result' : 'success' ,'user_id':user_info['id']} ,200

        



