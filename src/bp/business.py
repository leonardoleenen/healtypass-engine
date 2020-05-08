from flask import Flask, Blueprint, current_app, jsonify, request, send_file
import flask
import requests
import jwt
import os
import json
from services.business import create_cert_request


business_bp = Blueprint('api', 'bpm')

def clean_id(obj):
    obj['_id'] = str(obj['_id'])
    return obj

@business_bp.route("/isAlive",methods=['POST','OPTIONS'])
def is_alive():
    return "I'm alive from business Due"


@business_bp.route("/generate_request",methods=['POST','OPTIONS'])
def generate_request():
    success,result = create_cert_request(request.get_json())
    
    new_cert={
        "cid": result['cid']
    }

    if not success:
        return {
            'result':False,
            'error': result
        },422
    
    for key,value in result['payload'].items():
        new_cert[key]=value
       
    return {
        'result': success,
        'certificate': new_cert
    },200


@business_bp.route("/get_request",methods=['POST','OPTIONS'])
def get_request():
    return "Get Request"

