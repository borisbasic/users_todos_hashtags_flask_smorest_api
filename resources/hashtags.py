from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import HashtagModel, ToDoModel, UserModel
from schemas import HashtagSchema, ToDoSchema, UserSchema

blp = Blueprint('hastags', __name__, description='Operations under hashtags')

@blp.route('/hashtag')
class HashtagList(MethodView):
    @blp.response(200, HashtagSchema(many=True))
    def get(self):
        hashtags = HashtagModel.query.all()
        return hashtags
    
@blp.route('/hashtag/<string:hashtag_name>')
class Hashtag(MethodView):
    @blp.response(200, HashtagSchema)
    def get(self, hashtag_name):
        hashtag = HashtagModel.query.filter_by(hashtag='#'+hashtag_name).first_or_404()
        return hashtag
    
    def delete(self, hashtag_name):
        hashtag = HashtagModel.query.filter_by(hashtag='#'+hashtag_name).first_or_404()
        db.session.delete(hashtag)
        db.session.commit()
        return {'message':'Hashtag successfully deleted!'}
    
@blp.route('/user/todo/<int:todo_id>/hashtag')
class NewHashtag(MethodView):
    @jwt_required()
    @blp.arguments(HashtagSchema)
    @blp.response(201, ToDoSchema)
    def put(self, hashtag_data, todo_id):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        todo = user.todos.filter_by(id=todo_id).first_or_404()
        hashtags_ = HashtagModel.query.filter_by(hashtag='#'+hashtag_data['hashtag']).first()
        hashtags = []
        for hs in todo.hashtags.all():
            hashtags.append(hs.hashtag)

        if '#'+hashtag_data['hashtag'] in hashtags:
            abort(404, message='hashtag already exists')
        if hashtags_:
            todo.hashtags.append(hashtags_)
        else:
            hashtag_ = HashtagModel(hashtag='#'+hashtag_data['hashtag'])
            todo.hashtags.append(hashtag_)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured while loading data')
        
        return todo
    
    @jwt_required()
    @blp.arguments(HashtagSchema)
    @blp.response(201, ToDoSchema)
    def post(self, hashtag_data, todo_id):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        todo = user.todos.filter_by(id=todo_id).first_or_404()
        hashtags_ = HashtagModel.query.filter_by(hashtag='#'+hashtag_data['hashtag']).first()
        hashtags = []
        for hs in todo.hashtags.all():
            hashtags.append(hs.hashtag)
        
        if '#'+hashtag_data['hashtag'] in hashtags:
            abort(404, message='hashtag already exists')

        if hashtags_:
            todo.hashtags.append(hashtags_)
        else:
            hashtag_ = HashtagModel(hashtag='#'+hashtag_data['hashtag'])
            todo.hashtags.append(hashtag_)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured while loading data')

        return todo
    
@blp.route('/user/todo/<todo_id>/hashtag/<string:hashtag_name>')   
class HashtagA(MethodView):
    @jwt_required()
    def delete(self, todo_id, hashtag_name):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        todo = user.todos.filter_by(id=todo_id).first_or_404()
        hashtag = HashtagModel.query.filter_by(hashtag='#'+hashtag_name).first_or_404()
        todo.hashtags.remove(hashtag)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured while loading data')
        return {'messagge':'Hashtag deleted!'}
        



@blp.route('/todo/hashtag')
class HashtagsTodos(MethodView):
    @blp.arguments(HashtagSchema, location='query')
    @blp.response(200, ToDoSchema(many=True))
    def get(self, hashtag_data):
        todos = ToDoModel.query.all()
        print(todos)
        list_of_todos = []
        for todo in todos:
            print(todo)
            todo_ = todo.hashtags.filter_by(hashtag='#'+hashtag_data['hashtag']).first()
            if  todo_:
                print(todo_)
                list_of_todos.append(todo)
        if len(list_of_todos)>0:
            return list_of_todos
        else:
            abort(404, message='No such todos')

    


        

