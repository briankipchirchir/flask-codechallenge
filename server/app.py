#!/usr/bin/env python3

from flask import Flask, request, make_response,jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)  # Flask-RESTful API initialization

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# Hero Resource
class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

class HeroById(Resource):
    def get(self, hero_id):
        hero = db.session.get(Hero, hero_id)

        
        if not hero:
            return {"error": "Hero not found"}, 404

        
        serialized_hero = hero.to_dict()  

        # Add hero_powers to the serialized hero
        serialized_hero["hero_powers"] = [
            {
                "id": hp.id,
                "power": hp.power.name,  
                "strength": hp.strength
            } for hp in hero.hero_powers
        ]
        
        return serialized_hero, 200

# Power Resource
class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

class PowerById(Resource):
    def get(self, power_id):
        power = db.session.get(Power, power_id)

        if power:
            return jsonify(power.to_dict())
        return make_response({'error': 'Power not found'}, 404)

    def patch(self, power_id):
        power = db.session.get(Power, power_id)  # Replace this

        if not power:
            return make_response({'error': 'Power not found'}, 404)

        data = request.get_json()
        description = data.get('description')

        if description and len(description) >= 20:
            power.description = description
            db.session.commit()
            return jsonify(power.to_dict())
        return make_response({'errors': ['Validation errors']}, 400)

# HeroPower Resource
class HeroPowers(Resource):
    def post(self):
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        if strength not in ['Strong', 'Weak', 'Average']:
            return make_response({'errors': ['Validation errors']}, 400)

        hero_power = HeroPower(
            strength=strength,
            hero_id=hero_id,
            power_id=power_id
        )
        db.session.add(hero_power)
        db.session.commit()

        return jsonify(hero_power.to_dict())

# Register Resources
api.add_resource(Heroes, '/heroes')
api.add_resource(HeroById, '/heroes/<int:hero_id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowerById, '/powers/<int:power_id>')
api.add_resource(HeroPowers, '/hero_powers')

    




if __name__ == '__main__':
    app.run(port=5550, debug=True)