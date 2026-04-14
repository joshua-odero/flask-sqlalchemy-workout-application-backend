from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from marshmallow import Schema, fields

from datetime import date

db = SQLAlchemy()


# Define Models here
class Exercise(db.Model):
    
    __tablename__ = "exercises"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    #exercise.workouts
    workouts = db.relationship('Workout', secondary= "workout_exercises",
                back_populates = "exercises" )
    
    #validate category
    @validates('category')
    def validate_category(self, key, value):
        acceptedCategories = ["strength", "cardio", "flexibility"]

        if value not in acceptedCategories:
            return f"The category not found. The following are the accepted categories {acceptedCategories}"
        

    #validate name
    @validates('name')
    def validate_name(self, key, name):

        #check if it is not empty
        if not name:
            return f"The name cannot be empty"
        
        #check the length of the name
        if not 3 < len(name) < 20:
            return f"The number of characters should be between 3 and 20"
        

#create schema for exercise model
class ExerciseSchema(Schema):

    id = fields.Int(dump_only=True)
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()

    workouts = fields.Nested(lambda:WorkoutSchema (exclude=("exercises",)))


    
class Workout(db.Model):
    
    __tablename__ = "workouts"
    

    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    #workout.exercises
    exercises = db.relationship('Exercise', secondary = "workout_exercises",
                back_populates="workouts")
    
    @validates("date")
    def validate_date(self, key, value):
        
        #check if date is correct
        if value > date.today():
            raise("Date cannot be in future")

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        
        #check if the minutes are negative
        if value <= 0:
            raise("The duration must be positive")

#create schema for the workout model
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()

    exercises = fields.Nested(lambda:ExerciseSchema (exclude=("workouts",)))



class WorkoutExercise(db.Model):
    
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer,primary_key=True)
    workout_id = db.Column(db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    exercise = db.relationship('Exercise', back_populates= "workout_exercises")
    workout = db.relationship('Workout', back_populates= "workout_exercises")




