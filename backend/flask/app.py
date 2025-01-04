from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dataclasses import dataclass
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
import logging
import os
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

swagger = Swagger(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./db/todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@dataclass
class TodoItem(db.Model):
    __tablename__ = "todos"
    id: int
    title: str
    description: str

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, index=True)
    description = db.Column(db.String, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

# @app.before_first_request
# def create_tables():
#     db.create_all()


@app.route('/hello')
def hello():
    return 'world'

@app.route('/todos/', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = TodoItem(title=data['title'], description=data['description'])
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todos/', methods=['GET'])
def read_todos():
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    todos = TodoItem.query.offset(skip).limit(limit).all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/todos/<int:todo_id>', methods=['GET'])
def read_todo(todo_id):
    todo = TodoItem.query.get_or_404(todo_id)
    return jsonify(todo.to_dict())

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = TodoItem.query.get_or_404(todo_id)
    data = request.get_json()
    todo.title = data['title']
    todo.description = data['description']
    db.session.commit()
    return jsonify

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = TodoItem.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

@app.route("/spec")
def spec():
    return jsonify(swagger(app))

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)