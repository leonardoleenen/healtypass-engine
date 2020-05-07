from flask import Flask, Blueprint, current_app, jsonify, request, send_file
import flask
import requests
import jwt
import os
import json

business_bp = Blueprint('api', 'bpm')

@business_bp.route("/isAlive",methods=['POST','OPTIONS'])
def is_alive():
    return "I'm alive from business Due"