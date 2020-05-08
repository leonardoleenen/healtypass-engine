from pymongo import MongoClient
from bson import ObjectId
import os

MONGOURL = os.getenv('MONGODB_URL')
client = MongoClient(MONGOURL)
db = client[str(os.getenv('MONGODB_DB'))]

from .model import Model

class DefaultCertificate(Model):
    collection = db['defaultCertificate']

    @property
    def cid(self):
        return self._cid

    @cid.setter
    def cid(self,value):
        self._cid= value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,value):
        self._status= value
    
    @property
    def certKind(self):
        return self._certKind

    @certKind.setter
    def certKind(self,value):
        self._certKind= value

    @property
    def issuedOn(self):
        return self._issuedOn

    @issuedOn.setter
    def issuedOn(self,value):
        self._issuedOn= value
    
    @property
    def typeOfCertificate(self):
        return self._typeOfCertificate

    @typeOfCertificate.setter
    def typeOfCertificate(self,value):
        self._typeOfCertificate= value

    @property
    def authorizedUntil(self):
        return self._authorizedUntil

    @authorizedUntil.setter
    def authorizedUntil(self,value):
        self._authorizedUntil= value

    @property
    def authorizedUntil(self):
        return self._authorizedUntil

    @authorizedUntil.setter
    def authorizedUntil(self,value):
        self._authorizedUntil= value
    
