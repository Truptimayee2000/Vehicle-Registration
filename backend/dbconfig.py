from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


POSTGRES_URL = "localhost"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "Trupti"
POSTGRES_DB = "vahan"

DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}"

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'poolclass': NullPool}

db = SQLAlchemy(app)

engine = create_engine(DB_URL)

