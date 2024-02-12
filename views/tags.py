from flask.views import MethodView
from db import db
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import (
    TagsModel,
    StoresModel,
    ItemsTags,
    ItemsModel)
from schemaes import (
    TagSchema,
    ItemsAndTags,
    ItemSchema,
    ItemAndTagsSchema
)

blp = Blueprint('tags',__name__, description='operation on tags')


@blp.route('/store/<int:store_id>/tag')
class StoreIdTag (MethodView):

    @blp.response(200, TagSchema(many=True))
    def get (self, store_id):
        store = StoresModel.query.get_or_404(store_id)
        tags = store.tags
        return tags

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post (self, tag_data, store_id):
        if (TagsModel.query.filter(TagsModel.store_id == store_id , 
                                   TagsModel.name == tag_data['name']).first()):
            abort(400, message='this tag with that name already exist in store')
        if not tag_data.get('store_id'):
            tag_data['store_id'] = store_id
        tag = TagsModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(400)
        except SQLAlchemyError:
            abort(500)

        return tag

@blp.route('/tag/<int:tag_id>')
class Tag (MethodView):
    """
        get: get information about a specific tag
        delete: delete a tag from database if not link to item
    """

    @blp.response(200, TagSchema)
    def get (self, tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        return tag
    
    @blp.alt_response(404,description='in tag aslan vojod nadarad',example={'vaziyat':404,'mes':'nashod'})
    @blp.response(200,description='delete kardan ba movafaghiyat anjam shode',example={'message':'tag del'})
    @blp.alt_response(500,description='agar databse kar nakone',example={'vaziyat':500,'mes':'database rid'})
    def delete (self, tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        if tag.items :
            abort(400, message='you can not delete tag . this tag associate with a item')
        try:
            db.session.delete(tag)
            db.session.commit()
            return {'message': 'tag deleted.'}, 200
        except SQLAlchemyError as e:
            abort(500,message = str(e))


@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class ItemIdTagId (MethodView):
    """ post : link a tag to a item
        delete: unlink a tag from a item
    """

    @blp.response(200, TagSchema)
    def post (self,item_id, tag_id):
        item = ItemsModel.query.get_or_404(item_id)
        tag = TagsModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(400, message='tag and item are not belong to same store')

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return tag 

    @blp.response(200, ItemAndTagsSchema)
    def delete (self,item_id, tag_id):
        item = ItemsModel.query.get_or_404(item_id)
        tag = TagsModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return {"message":"unlink done with succeed","item":item,"tag":tag} 
