from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    pass

class Workout(db.model):
    pass

class WorkoutExercise(db.Model):
    pass

