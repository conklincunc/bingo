from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Identity 
from datetime import datetime, timedelta
import os
import uuid
import secrets

#dbf = 'db.db'
#engstr = f'sqlite:///{dbf}'
# TODO: replace this with connection env vars
db_user = os.environ.get('database-user')
db_password = os.environ.get('database-password')
db_host = os.environ.get('database-host')
db_port = os.environ.get('database-port')
db_name = os.environ.get('database-name')

#engstr = 'postgresql://dbadba:fofofofo@10.10.10.10:5432/bingo'
engstr = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

print(f"DEBUG: Engine String is {engstr}")

# settings from config.py
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engstr
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

################################################

class IdentitiesView(Resource):
    def get(self):
        identities = Identity.query.all()
        return {'Identities':list(x.json() for x in identities)}

    def post(self):
        data = request.get_json()
        uuid = GenerateUUID()
        key = GenerateKey()
        owner = data['owner']
        identity = Identity.query.filter_by(uuid=uuid).first()
        if identity:
            return {'message':'Identity already exists in database'},404
        new_identity = Identity(uuid, data['owner'], key)

        db.session.add(new_identity)
        db.session.commit()
        return new_identity.json(),201

class IdentityView(Resource):
    def get(self,uuid):
        identity = Identity.query.filter_by(uuid=uuid).first()
        if identity:
            return identity.json()
        return {'message':'Identity not found'},404

    def delete(self,uuid):

        identity = Identity.query.filter_by(uuid=uuid).first()
        if identity:
            db.session.delete(identity)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message': 'Identity not found'},404

# endpoints

# get all of the identity rows, post a new identity
api.add_resource(IdentitiesView, '/identities', methods=['GET', 'POST'])

# get the uuid info, delete the row of the uuid
api.add_resource(IdentityView,'/identity/<string:uuid>', methods=['GET', 'DELETE'])


# helper methods

def GenerateUUID():
    uuid = uuid.uuid4().hex
    print(f'DEBUG uuid: {uuid})
    return uuid

def GenerateKey():
    return secrets.token_urlsafe(16)


if __name__ == "__main__":
      app.run(host='0.0.0.0', debug=True, threaded=True, port=8080)
