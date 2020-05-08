
from .model import CrtRequest
import json 
from cid import make_cid
import multibase
from datetime import datetime
import threading

from .default_ca import DefaultCertificate

class providerThread(threading.Thread):
    def __init__(self, threadID, name, crt):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.crt : CrtRequest = crt

    def run(self):
        print ("Starting CA Default " + self.name)
      # process_data(self.name, self.q)
        certificate = DefaultCertificate()
        certificate.certKind="A"
        certificate.issuedOn=int(datetime.now().timestamp()) * 1000
        certificate.authorizedUntil=1596769200000
        certificate.issuedOn=1588905600973
        certificate.typeOfCertificate='PERMISO DE TRABAJO'
        certificate.authorizedSince=1591498800000
        certificate.status='APPROVED'
        cid= multibase.encode('base58btc',json.dumps(certificate)).decode("utf-8")
        certificate.cid=str(cid)
        certificate.save()
        self.crt.status="RESOLVED"
        self.crt.resolvedOn=int(datetime.now().timestamp()) * 1000
        self.crt.save()
        print ("Exiting CA Default " + self.name)


def create_cert_request(data):
    crt = CrtRequest()
    crt.issuedOn=int(datetime.now().timestamp()) * 1000
    crt.status='PENDING'
    crt.payload=data
    cid= multibase.encode('base58btc', json.dumps((crt)))
    crt.cid = cid.decode("utf-8")
    crt.save()

    thread = providerThread('xxx', 'caProvider', crt)
    thread.start()

    return True, crt