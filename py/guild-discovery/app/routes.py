from flask_cors import cross_origin
from flask import jsonify

from app import app
import time, scraper, matchmaker, subprocess, sys, os, pprint

from database.models import Guilds

class SessionStorage():
    allGuilds: []
    userSessionInfo: {}
    # session: {}

@app.before_first_request
def beforeReady():
     global data 
     data = SessionStorage()
     data.userSessionInfo = {}
     data.allGuilds = Guilds.objects
     pprint(data.allGuilds)

@app.route('/api/')
@cross_origin()
def getIndex():
    return jsonify(success=True), 200

@app.route('/api/guilds')
@cross_origin()
def getGuilds():
    return jsonify({'AllGuilds': data.allGuilds}), 200

@app.route('/api/store-user-preferences')
@cross_origin()
def storePreferencesForUser(sessionInfo):
    # TODO: eventually it might be nice to implement user login...
    #  but for now lets just use session storage on the client and here
    data.userSessionInfo = sessionInfo
    return jsonify(success=True), 200

@app.route('/api/user-correlations')
@cross_origin()
def getCorrelationsForUser():
    return jsonify({'UserCorrelation': matchmaker.getCorrelationsForUser(data.allGuilds, data.userSessionInfo)}), 200

