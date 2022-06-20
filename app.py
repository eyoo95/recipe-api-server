from flask import Config, Flask, jsonify, request
from http import HTTPStatus
from flask_restful import Api
from resources.recipe import RecipeListResource
from resources.recipe_info import RecipeResource
from resources.recipe_publish import RecipePublishResource
from resources.user import UserRegisterResource
from resources.user import UserLoginResource

app = Flask(__name__)

# 환경변수 세팅
app.config.from_object(Config)

# JWT 토큰 라이브러리 만들기


api = Api(app)

# 경로와 resource(API 코드)를 연결한다.
api.add_resource(RecipeListResource , '/recipes')
api.add_resource(RecipeResource , '/recipes/<int:recipe_id>')
api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
api.add_resource(UserRegisterResource, '/users/register')
api.add_resource(UserLoginResource, '/users/login')

if __name__ == '__main__' :
    app.run()