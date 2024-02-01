from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    serialize_rules= ('-hero_powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String, nullable= False)
    super_name = db.Column (db.String, nullable= False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now()) 
    hero_powers =  db.relationship('HeroPower', backref='hero')
    
    def __repr__ (self):
        return f"ID: {self.id} Name: {self.name} Super_name: {self.super_name}"

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    serialize_rules= ('-hero.hero_powers','-power.hero_powers')
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column (db.String, nullable= False)
    hero_id = db.Column (db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column (db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('strength')
    def check_validation(self, key,  value):
        if value != 'Strong' and value!= 'Weak' and value!= 'Average':
            raise  ValueError("Invalid strength level")
        return  value
    
    
    def __repr__ (self):
        return f"ID: {self.id} Strength: {self.strength} "
 
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    serialize_rules= ('-hero_powers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String, nullable= False)
    description = db.Column (db.String, nullable= False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now()) 
    hero_powers =  db.relationship("HeroPower", backref="power")
    
    # def serialize(self):
    #     return {"id": self.id , "name": self.name, "Description": self.description}

    @validates('description')
    def  validate_description(self, key, description):   
        if  description is None and len(description) <20 :
            raise ValueError ("Description must be atleast 20 characters long")
        return  description  
    
    def __repr__ (self):
        return f"ID: {self.id} Name: {self.name} Description: {self.description}"
