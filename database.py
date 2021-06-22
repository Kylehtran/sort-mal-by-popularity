from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Database(db.Model):
    
    ranking = db.Column(db.Integer, primary_key = True, unique = True)
    id = db.Column(db.Integer, unique = True)
    name = db.Column(db.String(150), unique = False)
    
    def __init__(self, ranking, id, name):
        
        self.ranking = ranking
        self.id = id
        self.name = name
        
    
    

