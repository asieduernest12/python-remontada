from flask import Flask, request, jsonify
from flask_restx import Resource, Api, fields
from sqlalchemy import Integer, String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_cors import CORS
from flask_alembic import Alembic
from pprint import pprint
import logging
import os

# from flask_swagger_ui import get_swaggerui_blueprint
# from flasgger import Swagger

app = Flask(__name__)
CORS(app)
api = Api(app)


# swagger = Swagger(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, './db/todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
# db = SQLAlchemy(app)
db.init_app(app)

alembic = Alembic()
alembic.init_app(app)

# # @dataclass
class Todo(db.Model):
    __tablename__ = 'todos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

with app.app_context():
    db.create_all()

TodoModel = api.model('TodoModel', {
        'id': fields.String,
        'title': fields.String,
        'description': fields.String
})

@api.route('/todos/<int:id>','/todos/', endpoint='Todos')
class TodoResource(Resource):

    @api.doc('hello')
    # @api.route('/hello')
    def hello(self):
        return 'world'

    @api.doc(model=[TodoModel],params={'limit':'count','skip':'skip count','id':'an id'},envelope=True)
    def get(self,id=None,skip=0,limit=10):
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 10, type=int)
        todoQuery = db.session.query(Todo)
        if id is None:
            todos = todoQuery.offset(skip).limit(limit).all()
            return jsonify([todo.to_dict() for todo in todos])
        else:
            todo = todoQuery.filter(Todo.id == id).first_or_404()
            return jsonify(todo.to_dict() if todo else {})

    @api.doc(body=TodoModel,model=TodoModel,envelope=True)
    def post(self):
        data = request.get_json()
        new_todo = Todo(
            title=data['title'],
            description=data['description']
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify(new_todo.to_dict())

    @api.doc(body=TodoModel,model=TodoModel)
    def patch(self,todo_id):
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json()
        todo.title = data['title']
        todo.description = data['description']
        db.session.commit()
        return jsonify(todo.to_dict())

    @api.doc(params={'ids':'itemId'},model=[TodoModel])
    def delete(self, id):
        todo = Todo.query.get_or_404(id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

@api.route('/items/',endpoint='items')
class Item(Resource):
    @api.doc()
    def get(self):
        return 'hello world'

# Swagger UI setup
# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'
# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Flask API"
#     }
# )


# app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(host='0.0.0.0', port=port, debug=debug)