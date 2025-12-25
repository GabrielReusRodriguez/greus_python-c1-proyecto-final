# Ponemos esto para evitar el error de dependencias circulares.
#from __future__ import annotations
from flask_sqlalchemy import SQLAlchemy

#import app

# Utilizo este script para inicializar la BBDD y evitar referencias circulares al hacer import

db = SQLAlchemy()