#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api,Resource
from werkzeug.exceptions import NotFound
# from sqlalchemy.ext.declarative import declarative_base

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# base = declarative_base()


migrate = Migrate(app, db)

db.init_app(app)

api= Api(app)

@app.errorhandler(NotFound)
def handle_not_found(e):
    response= make_response("NotFound: The requested resource not found", 404)
    return response

@app.route('/')
def home():
    return "Week 1 code challenge"

class Heroes(Resource):
    def get(self):
        response_dict= [n.to_dict() for n in Hero.query.all()]
        response= make_response(response_dict, 200)
        return  response

api.add_resource(Heroes, '/heroes')

class HeroesByID(Resource):
    def get(self,id):
        record=  Hero.query.filter_by(id=id).first()
        record_dict=  record.to_dict() if record else None
        if record is None:
            error_dict=  {"error": "Hero not found"}
            response= make_response(error_dict, 404 )
            return response
        else:
            response= make_response(record_dict, 200)
            return response
        
api.add_resource(HeroesByID, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        response_dict= [n.to_dict() for n in Power.query.all()]
        # response_dict= [n.serialize() for n in Power.query.all()]

        response= make_response(response_dict, 200)
        return  response

api.add_resource(Powers, '/powers')

class PowersByID(Resource):
    def get(self,id):
        record=  Power.query.filter_by(id=id).first()
        record_dict= record.to_dict() if record else None
        
        if record_dict== None:
            error_dict=  {'error': 'Power not found'}
            response= make_response(error_dict, 404)
            return response
        else:
            response= make_response(record_dict, 200)
            return response
    
    def patch(self,id):
        power = Power.query.filter_by(id=id).first()
        record_dict= power.to_dict() if power else None
        try:
            if record_dict== None:
                error_dict=  {'error': 'Power not found'}
                response= make_response(error_dict, 404)
                return response
            else:
                for attr in request.form:
                    setattr(power, attr, request.form[attr])
                
                db.session.add(power)
            
                db.session.commit()
                power_dict= power.to_dict()
                response= make_response(power_dict, 200)
                return response
        except:
            err_dict= {"errors" : ["validation errors"]}
            response= make_response(err_dict, 404)
            db.session.rollback()
            return response         

api.add_resource(PowersByID, '/powers/<int:id>')

class HeroPowers(Resource):

    def get(self):
        hero_power_dict = [r.to_dict() for r in HeroPower.query.all()] 
        if hero_power_dict:
            response= make_response(jsonify(hero_power_dict), 200)
            return response
        else:
            error_dict=  {'error': 'Hero power not found'}
            response= make_response(error_dict, 404)
            return response

    def post(self):
        try:
            # We are using this to allow us post JSON data from a react form.
            data= request.get_json() 
            
            # # strength= request.form['strength']
            # power_id=  int(request.form['power_id'])
            # hero_id=   int(request.form['hero_id'])
            strength= data.get("strength")
            power_id= data.get('power_id')
            hero_id=  data.get('hero_id')
            # )
            #Checking if power and hero exist
            power= Power.query.get(power_id)
            hero= Hero.query.get(hero_id)

            if not (power and hero):
                return make_response(jsonify({"errors": ["Power  or Hero does not exist."]}), 404)
            
            #Creating new hero power
            new_record= HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
            db.session.add(new_record)
            db.session.commit()
            
            hero_dict= hero.to_dict()

            response= make_response(jsonify(hero_dict), 201)
            return response
        except:
            err_dict= {"errors" : ["validation errors"]}
            response= make_response(err_dict, 404)
            db.session.rollback()
            return response  
    
api.add_resource(HeroPowers, '/hero_powers')   
     
if __name__ == '__main__':
    app.run(port=5555, debug=True)
