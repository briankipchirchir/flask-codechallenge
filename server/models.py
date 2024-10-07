from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)



class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationships
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete')
    powers = association_proxy('hero_powers', 'power')

    # Serialization rules
    serialize_rules = ('-hero_powers',)

    
    
    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # Relationship to HeroPower
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete')
    heroes = association_proxy('hero_powers', 'hero')

    # Serialization rules: Exclude hero_powers to ensure it's not part of the response
    serialize_rules = ('-hero_powers', '-heroes.hero_powers')

    # Validation for description (must be at least 20 characters)
    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return value

    def __repr__(self):
        return f'<Power {self.id}>'



class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)


    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Serialization rules
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    # Validation for strength (must be Strong, Weak, or Average)
    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError('Strength must be Strong, Weak, or Average')
        return value

    # add relationships

    # add serialization rules

    # add validation

    def __repr__(self):
        return f'<HeroPower {self.id}>'