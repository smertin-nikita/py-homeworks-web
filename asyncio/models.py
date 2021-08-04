from gino import Gino

db = Gino()


class SwPeople(db.Model):
    __tablename__ = 'sw_people'
    id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.String, nullable=False, default='None')
    eye_color = db.Column(db.String, nullable=False, default='None')
    films = db.Column(db.String, nullable=False, default='None')
    gender = db.Column(db.String, nullable=False, default='None')
    hair_color = db.Column(db.String, nullable=False, default='None')
    height = db.Column(db.Integer, nullable=False, default=0)
    homeworld = db.Column(db.String, nullable=False, default='None')
    mass = db.Column(db.String, nullable=False, default=0)
    name = db.Column(db.String, unique=True, nullable=False, default='None')
    skin_color = db.Column(db.String, nullable=False, default='None')
    species = db.Column(db.String, nullable=False, default='None')
    starships = db.Column(db.String, nullable=False, default='None')
    vehicles = db.Column(db.String, nullable=False, default='None')