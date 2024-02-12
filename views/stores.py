import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort , Blueprint
from schemaes import StoreSchema , UpdateStoreSchema, PlainStoreSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoresModel


blp = Blueprint('sotres', __name__, description= 'opration on stores')


@blp.route('/store')
class Store (MethodView):

    @blp.response(200, StoreSchema(many=True, exclude=('items',)))
    def get (self):
        return  StoresModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema )
    def post(self, store_data):
        # dont save same object
        store = StoresModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message = 'this store already exist in database')
        except SQLAlchemyError:
            abort(500, message = 'something goes wrong with database')
        return store

@blp.route('/store/<string:store_id>')
class StoreID (MethodView):

    @blp.response(200, StoreSchema)
    def get (self, store_id):
        #store = StoresModel.query.get_or_404(store_id)
        # or
        store = StoresModel.get_or_404(store_id)
        return store

    @blp.response(200, PlainStoreSchema)
    def delete (self, store_id):
        store = StoresModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return store
    
    @blp.arguments(UpdateStoreSchema)
    @blp.response(200, StoreSchema)
    def put (self,store_data, store_id):
        store = StoresModel.query.get_or_404(store_id)
        raise NotImplemented("not implement update function")