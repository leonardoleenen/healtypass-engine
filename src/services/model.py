from pymongo import MongoClient
from bson import ObjectId
import os

MONGOURL = os.getenv('MONGODB_URL')
client = MongoClient(MONGOURL)
db = client[str(os.getenv('MONGODB_DB'))]


class Model(dict):
    """
    A simple model that wraps mongodb document
    """
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self):
        if not self._id:
            self.collection.insert(self)
        else:
            self.collection.update(
                { "_id": ObjectId(self._id) }, self)

    def reload(self):
        if self._id:
            self.update(self.collection\
                    .find_one({"_id": ObjectId(self._id)}))

    def remove(self):
        if self._id:
            self.collection.remove({"_id": ObjectId(self._id)})
            self.clear()


class CrtRequest(Model):
    collection = db['crtRequest']

    @property
    def cid(self):
        return self._cid

    @cid.setter
    def cid(self,value):
        self._cid= value

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self,value):
        self._payload= value

    @property
    def issuedOn(self):
        return self._issuedOn

    @cid.setter
    def issuedOn(self,value):
        self._issuedOn= value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,value):
        self._status= value

    @property
    def resolvedOn(self):
        return self._resolvedOn

    @resolvedOn.setter
    def resolvedOn(self,value):
        self._resolvedOn= value


