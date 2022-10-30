from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from Model import db, Category, CategorySchema

from flask_httpauth import HTTPTokenAuth

categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()

auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "admin"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@auth.error_handler
def unauthorized():
    return {'error': 'Unauthorized access'}, 401


class CategoryResource(Resource):
    @auth.login_required
    def get(self):
        categories = Category.query.all()
        categories = categories_schema.dump(categories)
        return {'status': 'success', 'data': categories}, 200

    @auth.login_required
    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = category_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        category = Category.query.filter_by(name=data['name']).first()
        if category:
            return {'message': 'Category already exists'}, 400
        category = Category(
            name=json_data['name']
        )
        db.session.add(category)
        db.session.commit()

        result = category_schema.dump(category)

        return {"status": 'success', 'data': result}, 201

    @auth.login_required
    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = category_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        category = Category.query.filter_by(id=data['id']).first()

        if not category:
            return {'message': 'Category does not exist'}, 400
        category.name = data['name']
        db.session.commit()
        result = category_schema.dump(category)

        return {"status": 'success', 'data': result}, 204

    @auth.login_required
    def delete(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = category_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        category = Category.query.filter_by(id=data['id']).delete()
        db.session.commit()
        result = category_schema.dump(category)

        return {"status": 'success', 'data': result}, 204
