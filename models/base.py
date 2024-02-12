from db import db
from flask_smorest import abort

class ExtendModel():

    @classmethod
    def get_or_404(cls, primary_key):
        obj = db.session.get(cls, primary_key)
        return obj if obj else abort(404)
