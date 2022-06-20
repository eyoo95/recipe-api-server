from flask import Flask, jsonify, request
from http import HTTPStatus
from flask_restful import Api
from resources.recipe import RecipeListResource
from resources.recipe_info import RecipeResource
from resources.recipe_publish import RecipePublishResource

app = Flask(__name__)

api = Api(app)

# 경로와 resource(API 코드)를 연결한다.
api.add_resource(RecipeListResource , '/recipes')
api.add_resource(RecipeResource , '/recipes/<int:recipe_id>')
api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')

if __name__ == '__main__' :
    app.run()