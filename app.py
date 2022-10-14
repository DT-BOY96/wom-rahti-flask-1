from distutils.log import debug
import os, json, requests
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

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabin = db.Column(db.String, nullable=False)
    servicetype = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.Date, default = db.func.now())
    updated_at = db.Column(db.Date, 
        default = db.func.now(), 
        onupdate =db.func.now())

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cabin = db.Column(db.String, nullable=False)
    servicetype = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate =db.func.now())

#with app.app_context():
#   db.create_all()

@app.route("/cabins", methods=['GET', 'POST'])
def cabins():
    if request.method == "GET":
            print(os.environ.get('API_URL_ENV'))
            cabins = requests.get(os.environ.get('API_URL_ENV')+"/cabins/owned",
                headers= {request.headers.get('Authorization') })
               #headers= {"Authorization":"Bearer " +   request.headers.get('Authorization') })

            return cabins.json()


    if request.method == "POST":
        print("Login attempt")
        login = requests.get(os.environ.get('API_URL_ENV')+"/users/login",
        )

@app.route("/services", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def services():
    if request.method =='GET':
        try:
            services  = []
            for service in Service.query.all():
                services.append({
                    'id': service.id,
                    'cabin': service.cabin,
                    'servicetype': service.servicetype,
                    'price': service.price,
                    'updated_at': service.updated_at
                    })

            return services

        except: 
            return {"msg:" : "Could not find services"}
    
    if request.method == 'POST':
        try :
            body = request.get_json()
            new_service = Service(cabin=body['cabin'],servicetype=body['servicetype'],price=body['price'])
            db.session.add(new_service)
            db.session.commit()
            return { 'msg': 'Service created', 'id': new_service.id}
        except Exception as e: 
            return {"msg": "Enter valid info for all fields"}

    if request.method =='PATCH':
        try:
            body = request.get_json()
            update_service = Service.query.filter_by(id=body['id']).first()
            if(update_service == ""): 
                return {"msg": "No service found"}
            
            update_service.cabin = body['cabin']
            update_service.servicetype = body['servicetype']
            update_service.price = body['price']
            db.session.commit()
            return {
                'msg': 'You Patched something',
                'price': update_service.price
            }
        except:
            return {"msg": "Enter valid info for all fields"}
    if request.method =='DELETE':
        try:
            body = request.get_json()
            delete_service = Service.query.filter_by(id=body['id']).first()
            if(delete_service == ""):
                return {"msg": "No service found"}
            db.session.delete(delete_service)
            db.session.commit()
            

            return {
                'msg': 'You DELETED something',
                'id': delete_service.id
            }
        except: 
            return {"msg": "Could not delete"}
            
@app.route("/orders", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def orders():
    
    if request.method =='GET':
        try:
            orders  = []
            for order in Order.query.all():
                orders.append({
                    'id': order.id,
                    'cabin': order.cabin,
                    'servicetype': order.servicetype,
                    'date': order.date,
                    'updated_at': order.updated_at
                    })

            return orders
        except:
           return {"msg:" : "Could not find orders"} 
    
    if request.method == 'POST':
        try :
            body = request.get_json()
            new_order = Order(cabin=body['cabin'],servicetype=body['servicetype'],date=body['date'])
            db.session.add(new_order)
            db.session.commit()
            return { 'msg': 'Order created', 'id': new_order.id}
        except Exception as e: 
            return {"msg": "Enter valid info for all items"}

    if request.method =='PATCH':
        try:
            body = request.get_json()
            update_order = Order.query.filter_by(id=body['id']).first()
            if(update_order == ""):
                return {"msg": "No order found"}
            update_order.cabin = body['cabin']
            update_order.servicetype = body['servicetype']
            update_order.date = body['date']
            db.session.commit()
            return {
                'msg': 'You Patched something',
                'date': update_order.date
            }
        except:
            return {"msg": "Enter valid info for all fields"}    

    if request.method =='DELETE':
        try:
            body = request.get_json()
            delete_order = Order.query.filter_by(id=body['id']).first()
            db.session.delete(delete_order)
            db.session.commit()
            

            return {
                'msg': 'You DELETED something',
                'id': delete_order.id
            }
        except: 
            return {"msg": "Could not delete"}
    
if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
