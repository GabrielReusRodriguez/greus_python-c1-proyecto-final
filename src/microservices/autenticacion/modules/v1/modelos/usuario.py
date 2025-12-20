"""
Este script modela la entidad usuario. Es una clase que ejerce de ORM y abstrae la gestión de los datos con la BBDD.
"""
from flask_sqlalchemy import SQLAlchemy
from db import db

class Usuario(db.Model):
    """
        Usuario
            id_usuario (PK)
            username
            password
            rol (admin, medico, secretaria/o, paciente)
    """
    # Nombre de la tabla
    __tablename__ = 'usuarios'
    # Las columnas
    id_usuario = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)