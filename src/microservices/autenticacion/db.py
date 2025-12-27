from flask_sqlalchemy import SQLAlchemy

# Utilizo este script para inicializar la BBDD y evitar referencias circulares al hacer import
db = SQLAlchemy()