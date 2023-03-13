import os
from datetime import timedelta
#for creating SECRET_KEY we can use python module SECRETS, like secrets.SystemRandom().getrandbits(128)
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db
from flask_jwt_extended import get_jwt_identity, get_jwt
import models
from models import UserModel, Blocklist
from resources.to_do import blp as ToDoBlueprint
from resources.hashtags import blp as HashtagsBlueprint
from resources.user import blp as UserBlueprint

def create_app():
    app = Flask(__name__)

    app.config['API_TITLE'] = 'USERS-TODO-HASHTAG REST API' 
    app.config['API_VERSION'] = 'v1' 
    app.config['OPENAPI_VERSION'] = '3.0.3' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    app.config['JWT_SECRET_KEY']='my_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(hours=1)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        blocklist_token = Blocklist.query.filter_by(jti=jti).first()
        if blocklist_token:
            return True
        else:
            return False

    @jwt.user_lookup_loader  #GET CURRENT USER
    def user_lookup_callback(jwt_header, jwt_payload):
        user_id = jwt_payload['sub']
        return UserModel.query.get_or_404(user_id)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({'description':'Request does not contain an access token', 'error':'authorizatiion_required'}))

    @jwt.invalid_token_loader
    def invalid_token_callbak(error):
        return (jsonify({'message':'Signature verification failed','error':'invalid token'}), 401,)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(jsonify({'message':'The token has expired', 'error':'token_expired'}), 401,)

    api.register_blueprint(ToDoBlueprint)
    api.register_blueprint(HashtagsBlueprint)
    api.register_blueprint(UserBlueprint)
    return app