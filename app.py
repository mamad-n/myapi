import os
from flask import Flask 
from flask.json import jsonify
from flask_smorest import Api
from views import items_blueprint, stores_blueprint, tags_blueprint,users_blueprint
from db import db
from flask_jwt_extended import JWTManager
import models
from datetime import timedelta
from flask_migrate import Migrate
from dotenv import load_dotenv
from blocklist import BLOCKLIST


def create_app(db_uri=None):
    app = Flask(__name__)
    load_dotenv()
    app.config['PROPAGATE_EXCEPTIONS']= True
    app.config["API_TITLE"] = "My API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.0/'
    # config database
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri or os.getenv("DATABASE_URI", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    # user flask-migrate
    migrate = Migrate(app, db)
    
    app.config['JWT_SECRET_KEY'] = 'raz'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=30)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def custom_unauthorized_loader(x):
        return jsonify({'message':'pleas send correct access token to me'}), 401

    @jwt.expired_token_loader
    def custome_expired_token_loader(x,y):
        return jsonify({'message':'tokenet monghzi shode'}), 401

    @jwt.invalid_token_loader
    def cusotme_invalid_token_loader(x):
        return jsonify({'message':'token-e dorosti nadadi'})

    @jwt.additional_claims_loader
    def custome_additional_claims_loader(x):
        admin = False
        if x == 1:
            admin = True
        return {'admin_per': admin}

    @jwt.token_in_blocklist_loader
    def custome_token_in_blocklist_loader(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token (jwt_header, jwt_payload):
        return jsonify({'messsage':'the token is revoked . please loginin again'}), 401
 

    api = Api(app)
    api.register_blueprint(items_blueprint)
    api.register_blueprint(stores_blueprint)
    api.register_blueprint(tags_blueprint)
    api.register_blueprint(users_blueprint)

    return app



