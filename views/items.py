from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemaes import ItemSchema, UpdateItemSchema,PlainItemSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import ItemsModel, StoresModel  
from flask_jwt_extended import jwt_required


blp = Blueprint('items', __name__, description= 'operation on items')

@blp.route('/item')
class Item (MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get (self):
        return ItemsModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    @jwt_required()
    def post(self, item_data):
        # dont save same object
        item = ItemsModel(**item_data)

        # check 'store_id' is valid or not
        store = StoresModel.query.get_or_404(item.store_id)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort (400, message = 'this item is already exist in database')
        except SQLAlchemyError:
            abort(500, message = 'somethin goes wron in database')

        return item

@blp.route('/item/<string:item_id>')
class ItemId (MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema)
    def get (self, item_id):
        item = ItemsModel.query.get_or_404(item_id)
        # or
        #item = ItemsModel.get_or_404(item_id)

        return item

    @blp.response(200, PlainItemSchema(exclude=('store_id',)))
    def delete(self, item_id):
        item = ItemsModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return item

    @blp.arguments(UpdateItemSchema)
    @blp.response(200, ItemSchema)
    def put (self,item_data, item_id):
        item = ItemsModel.query.get(item_id)
        if item:
            item.name = item_data['name']
            item.price = item_data['price']
        else:
            # client must insert 'store_id' in its request
            item = ItemsModel(id = item_id, **item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message = 'this item is identical with item in database')
        except SQLAlchemyError:
            abort(500, message = 'somethin goes wrong with database')

        return item
