from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user, get_jti, get_csrf_token,\
get_jwt_header, get_jwt_request_location, current_user
from sqlalchemy.exc import SQLAlchemyError

from db import db

from schemas import ToDoSchema, UserSchema
from models import ToDoModel
from models import HashtagModel
from models import UserModel
blp = Blueprint('todos', __name__, description='Operations with todos')

@blp.route('/user/todo')
class UserToDoList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        
        print(current_user.todos.all())
        return user
    
    @jwt_required()
    @blp.arguments(ToDoSchema)
    @blp.response(201, UserSchema)
    def post(self, todo_data):
        user_id = get_jwt_identity()
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        todo = ToDoModel(to_do=todo_data['to_do'], date=todo_data['date'], user_id=user_id)
        user.todos.append(todo)
        for hs in todo_data['hashtags']:
            hashtag_ = HashtagModel.query.filter_by(hashtag='#'+hs['hashtag']).first()
            if hashtag_:
              todo.hashtags.append(hashtag_)
            else:
                hashtag_ = HashtagModel(hashtag='#'+hs['hashtag'])
                todo.hashtags.append(hashtag_) 
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured while loading data')
        return user
       
        
         
        


@blp.route('/user/todo/<int:todo_id>')
class UserTodo(MethodView):
    @jwt_required()
    @blp.response(200, ToDoSchema)
    def get(self, todo_id):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        todo = user.todos.filter_by(id=todo_id).first()
        return todo
    
    @jwt_required()
    def delete(self, todo_id):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        print(user)
        todo = user.todos.filter_by(id=todo_id).first()
        print
        try:
            db.session.delete(todo)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured while loading data')
        return {'message': 'ToDo is deleted!'}
    

    @jwt_required()
    @blp.arguments(ToDoSchema)
    @blp.response(200, ToDoSchema)
    def put(self, todo_data, todo_id):
        user_id = get_jwt_identity()
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        todo = user.todos.filter_by(id=todo_id).first()
        if todo:
            todo.to_do = todo_data['to_do']
            todo.date = todo_data['date']
            for hs in todo.hashtags:
                todo.hashtags.remove(hs)
            for hs in todo_data['hashtags']:
                hashtag_ = HashtagModel.query.filter_by(hashtag='#'+hs['hashtag']).first()
                if hashtag_:
                    todo.hashtags.append(hashtag_)
                else:
                    hashtag_ = HashtagModel(hashtag='#'+hs['hashtag'])
                    todo.hashtags.append(hashtag_)
        else:
            todo = ToDoModel(id=todo_id, to_do=todo_data['to_do'], date=todo_data['date'], user_id=user_id)
            user.todos.append(todo)
            for hs in todo_data['hashtags']:
                hashtag_ = HashtagModel.query.filter_by(hashtag='#'+hs['hashtag']).first()
                if hashtag_:
                    todo.hashtags.append(hashtag_)
                else:
                    hashtag_ = HashtagModel(hashtag='#'+hs['hashtag'])
                    todo.hashtags.append(hashtag_)

        db.session.add(user)
        db.session.commit()
        return todo
    

@blp.route('/todo/<int:todo_id>')
class ToDo(MethodView):
    @blp.response(200, ToDoSchema)
    def get(self, todo_id):
        todo = ToDoModel.query.get_or_404(todo_id)
        return todo
    
@blp.route('/todo')
class ToDoList(MethodView):
    @blp.response(200, ToDoSchema(many=True))
    def get(self):
        todos = ToDoModel.query.all()
        return todos