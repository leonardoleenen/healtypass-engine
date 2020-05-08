
from .model import CrtRequest
import json 
from cid import make_cid
import multibase
from datetime import datetime

def create_cert_request(data):
    cid= multibase.encode('base58btc', json.dumps((data)))
    crt = CrtRequest()
    crt.cid = cid.decode("utf-8")
    crt.issuedOn=int(datetime.now().timestamp()) * 1000
    crt.payload=data
    crt.save()

    return True, crt