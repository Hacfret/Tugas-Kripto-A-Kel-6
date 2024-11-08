# Pemrograman Jaringan A
# Anggorta Kelompok 5:
# Dhammas Sachita - 21120121130081
# Fadhil Hadrian Azzami - 21120121130120
# Muhammad Fathan Mubiina - 21120121140164
# Arradhin Zidan Ilyasa Subiyantoro - 21120121140097
# Ahmad Rizqy Yourin - 21120121140136

#Credit : https://github.com/gitdagray/python-flask-rest-api/blob/main/api.py

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(80), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

# Email validation
def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

# Parser
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}

# Helper function to add user
def add_user(name, email):
    if not is_valid_email(email):
        abort(400, message="Invalid email format.")
    if UserModel.query.filter_by(email=email).first():
        abort(409, message="Email already exists.")
    user = UserModel(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return user

# Resources
class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = add_user(args["name"], args["email"])
        return user, 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message=f"User with id {id} not found.")
        return user

    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.get(id)
        if not user:
            abort(404, message=f"User with id {id} not found.")
        if args['name']:
            user.name = args['name']
        if args['email']:
            if not is_valid_email(args['email']):
                abort(400, message="Invalid email format.")
            user.email = args['email']
        db.session.commit()
        return user

    @marshal_with(user_fields)
    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message=f"User with id {id} not found.")
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User with id {id} deleted successfully.'}, 200

class UserByName(Resource):
    @marshal_with(user_fields)
    def get(self, name):
        user = UserModel.query.filter_by(name=name).first()
        if not user:
            abort(404, message=f"User with name {name} not found.")
        return user

# API Endpoints
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(UserByName, '/api/users/name/<string:name>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)



