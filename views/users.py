from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemaes import UserSchema
from models import UsersModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha512
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    create_refresh_token,
    get_jwt_identity
)
from blocklist import BLOCKLIST
from db import db


blp = Blueprint('users', __name__, description='opration on users')

@blp.route('/register')
class userregister (MethodView):
    
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post (self,user_data:dict):
        password = user_data['password']
        user_data.update(password=pbkdf2_sha512.hash(password))
        user = UsersModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message='this user already exist in database')
        except SQLAlchemyError as e:
            abort(500, message =str(e))

        return user
    
@blp.route('/user/<int:user_id>')
class userId (MethodView):
    """ 
        2 'method'-e zir faghat baray 'developer' ijad shode ta rahat betavanad
        ba 'api' kar konad va dar zamane 'deploy' bayad in 'endpoint'-ha ra 'delete' konid
    """
    @blp.response(200, UserSchema)
    def get (self,user_id):
        user = UsersModel.query.get_or_404(user_id)

        return user

    
    def delete(self,user_id):
        user = UsersModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500)
        
        return {'message':'user deleted.'}

@blp.route('/login')
class userlogin (MethodView):

    @blp.arguments(UserSchema)
    def post (self,user_data):
        user = UsersModel.query.filter(UsersModel.username == user_data['username']).first()

        if user and pbkdf2_sha512.verify(user_data['password'],user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access-token': access_token,'refresh-token': refresh_token}
            
        abort(400, message = 'invalid credintials')

@blp.route('/logout')
class userlogout (MethodView):

    @jwt_required()
    def get (self):
        BLOCKLIST.add(get_jwt().get('jti'))
        return {'message':'logout now'}, 200
    
@blp.route('/refresh')
class refreshtoken (MethodView):

    @jwt_required(refresh=True)    
    def post (self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)

        return {'access-token': access_token}




