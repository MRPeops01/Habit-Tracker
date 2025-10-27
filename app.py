import os
from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Create a global MongoClient with TLS for secure connection
MONGO_URI = os.environ.get("MONGODB_URI")
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=False,  # keep False if your Atlas certs are valid
    serverSelectionTimeoutMS=30000      # 30-second timeout
)

db = client.get_default_database()


def create_app():
    app = Flask(__name__)

    # Attach the preconfigured database client to the app
    app.db = db

    # Register routes blueprint
    app.register_blueprint(pages)

    return app
