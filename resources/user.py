from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from db import db

from schemas import RegisterSchema, UserSchema, LoginSchema
from models import UserModel, Blocklist

blp = Blueprint('users', __name__, description='Operations with users')

@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(RegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(409, message='User with that name exists')
        if UserModel.query.filter(UserModel.email == user_data['email']).first():
            abort(409, message='User with that email exists')
        user = UserModel(username=user_data['username'], email=user_data['email'], password=pbkdf2_sha256.hash(user_data['password']))
       
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured while loading data')
        return {'message':'User created successfully!'}
    


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(or_(UserModel.username==user_data['username'], UserModel.email==user_data['email'])).first()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            acces_token = create_access_token(identity=user.id)
            return {'message':'User logged!','access_token':acces_token}
        else:
            abort(401, message='Invalid credintials!')


@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        blocklisted_token = Blocklist(jti=jti)
        try:
            db.session.add(blocklisted_token)
            db.session.commit()
            blocklisted_tokens = Blocklist.query.all()
            for bt in blocklisted_tokens:
                print(bt.jti)
            return {'message':'Successfully logged out!'}
        except SQLAlchemyError:
            abort(401, message='Something went wrong')


@blp.route('/user')
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        user = UserModel.query.all()
        return user
    
@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message':'User deleted!'}
