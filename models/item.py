from db import db
from models.base import ExtendModel

class ItemsModel (db.Model,ExtendModel):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True , nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), unique=False, nullable=False)
    store = db.relationship("StoresModel", back_populates = "items")
    tags = db.relationship("TagsModel", back_populates="items", secondary = 'itemstags')