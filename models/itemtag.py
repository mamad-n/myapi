from db import db

class ItemsTags (db.Model):
    __tablename__ = 'itemstags'

    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))