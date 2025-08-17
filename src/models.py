from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    
    # Relaciones con favoritos
    favorite_characters = relationship('FavoriteCharacter', back_populates='user', cascade='all, delete-orphan')
    favorite_planets = relationship('FavoritePlanet', back_populates='user', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None,
            "is_active": self.is_active
        }

class Character(db.Model):
    __tablename__ = 'character'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[str] = mapped_column(String(10), nullable=True)
    mass: Mapped[str] = mapped_column(String(10), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    homeworld_id: Mapped[int] = mapped_column(db.ForeignKey('planet.id'), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relaciones
    homeworld = relationship('Planet', back_populates='residents')
    favorited_by = relationship('FavoriteCharacter', back_populates='character', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld_id": self.homeworld_id,
            "description": self.description
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(20), nullable=True)
    orbital_period: Mapped[str] = mapped_column(String(20), nullable=True)
    diameter: Mapped[str] = mapped_column(String(20), nullable=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    gravity: Mapped[str] = mapped_column(String(50), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    surface_water: Mapped[str] = mapped_column(String(20), nullable=True)
    population: Mapped[str] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relaciones
    residents = relationship('Character', back_populates='homeworld')
    favorited_by = relationship('FavoritePlanet', back_populates='planet', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "description": self.description
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('character.id'), nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = relationship('User', back_populates='favorite_characters')
    character = relationship('Character', back_populates='favorited_by')
    
    # Constraint para evitar favoritos duplicados
    __table_args__ = (
        db.UniqueConstraint('user_id', 'character_id', name='unique_favorite_character'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "date_added": self.date_added.isoformat() if self.date_added else None,
            "character": self.character.serialize() if self.character else None
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey('planet.id'), nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = relationship('User', back_populates='favorite_planets')
    planet = relationship('Planet', back_populates='favorited_by')
    
    # Constraint para evitar favoritos duplicados
    __table_args__ = (
        db.UniqueConstraint('user_id', 'planet_id', name='unique_favorite_planet'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "date_added": self.date_added.isoformat() if self.date_added else None,
            "planet": self.planet.serialize() if self.planet else None
        }