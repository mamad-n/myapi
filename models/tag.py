from db import db

class TagsModel (db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'),unique=False, nullable=False)
    store = db.relationship('StoresModel', back_populates='tags')
    items = db.relationship('ItemsModel', back_populates='tags', secondary = 'itemstags')