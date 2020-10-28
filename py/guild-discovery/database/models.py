#~guild-discovery/database/models.py
from .db import db

class Guilds(db.Document):
    guildID = db.IntField( required=True, unique=True )
    name = db.StringField( required=True )
    master = db.StringField( required=True )
    tag = db.StringField()
    race = db.StringField()
    members = db.IntField( required=True )
    totalPoints = db.IntField()
    avgPoints = db.IntField()
    description = db.StringField()
    lieutenants = db.ListField(db.StringField())
    guildMembers = db.ListField(db.StringField())
    bannerDisplayTemplate = db.StringField()