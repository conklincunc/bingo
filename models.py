from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
db = SQLAlchemy()


class Identity(db.Model):
    __tablename__ = 'identity'

    uuid = db.Column(db.String(32), primary_key=True)
    owner = db.Column(db.String(64))
    key = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=False)
    data_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, uuid, owner, key): 
        self.uuid = uuid 
        self.owner = owner 
        self.key = key 

    def json(self):
        return {"uuid":self.uuid,"owner":self.owner, "key": self.key, "active":self.active,
                "data_date":str(self.data_date)}
