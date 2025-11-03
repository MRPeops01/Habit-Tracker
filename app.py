import os
import sys
import logging
from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Configure MongoDB connection
# -----------------------------
MONGO_URI = os.environ.get("MONGODB_URI", "").strip()  # Remove trailing whitespace/newlines

if not MONGO_URI:
    logging.error("MONGO_URI environment variable is not set!")
    sys.exit(1)

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=False,  # keep False if Atlas certs are valid
        serverSelectionTimeoutMS=30000      # 30-second timeout
    )
    # Test connection immediately
    client.admin.command("ping")
    logging.info("MongoDB connection successful.")

    # Explicitly select your database
    db = client["habit_tracker"]

except Exception:
    logging.exception("Failed to connect to MongoDB")
    sys.exit(1)

# -----------------------------
# Flask app factory
# -----------------------------
def create_app():
    app = Flask(__name__)

    # Attach the preconfigured database client to the app
    app.db = db

    # Register routes blueprint
    app.register_blueprint(pages)

    # Optional: enable debug locally
    if os.environ.get("FLASK_DEBUG") == "1":
        app.config['DEBUG'] = True

    return app

# -----------------------------
# Run locally for testing
# -----------------------------
if __name__ == "__main__":
    try:
        app = create_app()
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
    except Exception:
        logging.exception("App failed to start")
        sys.exit(1)
