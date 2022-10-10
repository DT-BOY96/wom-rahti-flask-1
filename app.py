import os
from flask import Flask, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

# create the extension
db = SQLAlchemy()
#SQLAlchemy (postgresql)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URL')
# initialize the app with the extension
db.init_app(app)

#datamodell = table i postgresql
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, 
        default = db.func.now(), 
        onupdate =db.func.now())

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabin = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, 
        default = db.func.now(), 
        onupdate =db.func.now())

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabin = db.Column(db.String, nullable=False)
    servicetype = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, 
        default = db.func.now(), 
        onupdate =db.func.now())

#with app.app_context():
#   db.create_all()

@app.route("/", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def index():
    if request.method == 'GET':
        return { 
            'method': request.method,
            'msg': 'GitHUb Webhook deployment works!', 
            'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR') 
        }

    if request.method ==['POST']:
        body = request.get_json()

        return {
            'msg': 'You POSTED something',
            'request_body': body
        }

    if request.method =='PATCH':
        body = request.get_json()

        return {
            'msg': 'You Patched something',
            'request_body': body
        }
    
    if request.method =='DELETE':
        body = request.get_json()

        return {
            'msg': 'You DELETED something',
            'request_body': body
        }


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method =='GET':
        users  = []
        for user in User.query.all():
            users.append({
                'id': user.id,
                'email': user.email,
                'updated_at': user.updated_at
                })
        return users
    
    if request.method == 'POST':
        body = request.get_json()
        new_user = User(email=body['email'])
        db.session.add(new_user)
        db.session.commit()
        return { 'msg': 'User created', 'id': new_user.id}
    

@app.route("/orders", methods=['GET', 'POST'])
def services():
    if request.method =='GET':
        users  = []
        for user in User.query.all():
            users.append({
                'id': user.id,
                'email': user.email,
                'updated_at': user.updated_at
                })
        return users
    
    if request.method == 'POST':
        body = request.get_json()
        new_user = User(email=body['email'])
        db.session.add(new_user)
        db.session.commit()
        return { 'msg': 'User created', 'id': new_user.id}
    
if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
