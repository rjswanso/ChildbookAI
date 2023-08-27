from datetime import datetime
from app import db

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    story_synopsis  = db.Column(db.String, nullable=True)
    story_section_titles = db.Column(db.String, nullable=True)
    story_section_chunks = db.Column(db.String, nullable=True)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'{self.title} created on {self.date}'

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.String, nullable=False)
    urls = db.Column(db.String, nullable=True)