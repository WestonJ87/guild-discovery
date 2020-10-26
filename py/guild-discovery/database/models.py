#~guild-discovery/database/models.py
from .db import db

class Guilds(db.Document):
    guildID = db.IntField( required=True, unique=True )
    name = db.StringField( required=True )
    master = db.StringField( required=True )
    tag = db.StringField()
    race = db.StringField()
    members = db.StringField( required=True )
    totalPoints = db.StringField()
    avgPoints = db.StringField()
    description = db.StringField()
    lieutenants = db.ListField(db.StringField())
    guildMembers = db.ListField(db.StringField())