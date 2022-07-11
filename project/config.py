import os


basedir = os.path.abspath(os.path.dirname(__file__))
uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
if not uri:
    uri = "postgresql://users_be:users_be@localhost:5432/users_be_dev"


class Config(object):
    SQLALCHEMY_DATABASE_URI = uri
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FIREBASE_TYPE = os.getenv("FIREBASE_TYPE")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY_ID = os.getenv("FIREBASE_PRIVATE_KEY_ID")
    FIREBASE_PRIVATE_KEY = f"-----BEGIN PRIVATE KEY-----\n{os.getenv('FIREBASE_PRIVATE_KEY')}\n-----END PRIVATE KEY-----\n".replace(
        "\\n", "\n"
    )
    FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")
    FIREBASE_CLIENT_ID = os.getenv("FIREBASE_CLIENT_ID")
    FIREBASE_AUTH_URI = os.getenv("FIREBASE_AUTH_URI")
    FIREBASE_TOKEN_URI = os.getenv("FIREBASE_TOKEN_URI")
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.getenv(
        "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
    )
    FIREBASE_CLIENT_X509_CERT_URL = os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
    FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")
    STORAGE_BUCKET = os.getenv("STORAGE_BUCKET")


class ConfigTest(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://test_user:test_pass@db_test:5433/test_db"
    SECRET_KEY = "bad_secret_key"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True
    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False
