from flask_cors import cross_origin
from flask import jsonify

from app import app
import time
import scraper

from database.models import Guilds

class SessionStorage():
    allGuilds: []
    # session: {}

@app.before_first_request
def beforeReady():
     global data 
     data = SessionStorage()
     data.allGuilds = Guilds.objects
     
@app.route('/')
@cross_origin()
def getIndex():
    return jsonify(success=True), 200

@app.route('/guilds')
@cross_origin()
def getGuilds():
    return jsonify(data.allGuilds), 200

@app.route('/guilds/<id>')
@cross_origin()
def getDetailedGuildPage(id):
    return jsonify(scraper.getGuildPage(id), 200)
