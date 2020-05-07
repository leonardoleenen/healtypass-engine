# -*- coding: utf-8; -*-

# System
import os

# Flask
from flask import Flask, request, jsonify
from flask_cors import cross_origin
import sys
import json
from flask_talisman import Talisman
from bp.business import business_bp
from dotenv import load_dotenv
from flask_cors import CORS

import requests
import os

load_dotenv()

# App definition
app = Flask('healthypass-engine')
app.secret_key = 'healthypass-engine'

''' 
feature_policy = {
    'accelerometer': '\'none\'',
    'ambient-light-sensor': '\'none\'',
    'autoplay': '\'none\'',
    'battery': '\'none\'',
    'camera': '\'none\'',
    'display-capture': '\'none\'',
    'document-domain': '\'none\'',
    'encrypted-media': '\'none\'',
    'fullscreen': '\'none\'',
    'geolocation': '\'none\'',
    'gyroscope': '\'none\'',
    'layout-animations': '\'none\'',
    'legacy-image-formats': '\'none\'',
    'magnetometer': '\'none\'',
    'microphone': '\'none\'',
    'midi': '\'none\'',
    'oversized-images': '\'none\'',
    'payment': '\'none\'',
    'picture-in-picture': '\'none\'',
    'usb': '\'none\'',
    'vr': '\'none\'',
    'wake-lock': '\'none\'',
    'xr-spatial-tracking': '\'none\''
}
Talisman(app, feature_policy=feature_policy)
''' 

# Blue Prints
app.register_blueprint(business_bp, url_prefix='/api')


''' 
@app.before_request
def before_request():
    origins = get_allow_origins()
    if len(origins)==0:
        set_default_allow_origin()
        return

    if '*' in origins:
        print('WARNING!!! el servicio se encuentra expuesto. Deben agregar en la colleción settings un atributo llamado allowOrigins con los host (separados por coma) que están autorizados a ingresar')
        return

    if len(list(filter(lambda  x:  x == request.headers['host'], origins))) ==0 :
       
        return 'False',403
''' 

'''
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
'''

@app.route("/api/alive", methods=['POST','OPTIONS'])
def alive():
    return 'Its alive'
    # return str(dbs)


def init():
    pass

def start_local_server():
    init()
    app.app_context().push()
    app.config['CORS_HEADERS'] = 'Content-Type'
    if os.getenv('FLASK_ENV') == 'development':
        app.run("0.0.0.0", os.getenv('PORT'),debug=os.getenv('DEBUG'),ssl_context=('crt.txt', 'key.txt'))
    else:
         app.run("0.0.0.0", os.getenv('PORT'),debug=os.getenv('DEBUG'))
if __name__ == '__main__':
    start_local_server()
    with app.app_context():
        init()
