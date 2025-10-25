import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
app.db = client.get_default_database()

# Import blueprint from routes.py
from routes import pages
app.register_blueprint(pages)

if __name__ == "__main__":
    app.run(debug=True)
