from hashlib import sha256

from flask import Flask, request
from flask_restful import Api, Resource

from web_app import errors, services, constant
from web_app.dao import Dao

app = Flask(__name__)
api = Api(app)

dao = Dao(constant.SHELVE_FILENAME)


class MessageResource(Resource):

    def get(self, message_id=None):
        try:
            message = dao.retrieve(message_id)
            return {message_id: message}, 200

        except errors.NotFoundError:
            return {'error': f'Not Found: "{message_id}"'}, 404

    def put(self, message_id: str):
        data = request.form['message']

        try:
            dao.update(message_id, data)

            return 'Updated', 200
        except errors.NotFoundError:
            return {'error': f'Not Found: "{message_id}"'}, 404

    def post(self, message_id: str):
        message = request.form['message']
        try:
            dao.create(message_id, message)

            return {'message': 'created'}, 201
        except errors.AlreadyExists:
            return {'error': f'Already exists: "{message_id}"'}, 406

    def delete(self, message_id: str):
        try:
            dao.delete(message_id)

            return '', 200
        except errors.NotFoundError:
            return {'error': f'Not Found: "{message_id}"'}, 404


class TokenResource(Resource):

    def get(self, idul: str):
        if services.user_exists(idul):
            return services.get_token(), 200

        return '', 404

    def post(self, idul):

        return {'token': sha256(idul)}


api.add_resource(MessageResource, '/api/messages/<string:message_id>')
api.add_resource(TokenResource, '/api/token/<string:idul>')

if __name__ == '__main__':
    app.run()
