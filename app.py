import os

import firebase_admin
from firebase_admin import auth, credentials
from flask import jsonify, request

from project import create_app, db
from project.config import Config

# Call the application factory function to construct a Flask application
# instance using the development configuration
app = create_app("project.config.Config")

cred = credentials.Certificate(
    {
        "type": Config.FIREBASE_TYPE,
        "project_id": Config.FIREBASE_PROJECT_ID,
        "private_key_id": Config.FIREBASE_PRIVATE_KEY_ID,
        "private_key": Config.FIREBASE_PRIVATE_KEY,
        "client_email": Config.FIREBASE_CLIENT_EMAIL,
        "client_id": Config.FIREBASE_CLIENT_ID,
        "auth_uri": Config.FIREBASE_AUTH_URI,
        "token_uri": Config.FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url": Config.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": Config.FIREBASE_CLIENT_X509_CERT_URL,
    }
)
firebase_admin.initialize_app(cred)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
