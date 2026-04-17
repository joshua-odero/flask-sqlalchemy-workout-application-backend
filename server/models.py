from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from marshmallow import Schema, ValidationError, fields, validates_schema
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


# Define Models here
class Exercise(db.Model):
    
    __tablename__ = "exercises"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)


    # Association proxy to get workouts for an exercise through workout_exercises table
    workouts = association_proxy('workout_exercises', 
                                 'workout', 
                                 creator=lambda workout_obj: WorkoutExercise(workout=workout_obj))
    
    #define a relationship with the association table => workout_exercise.exercise
    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates='exercise', 
        cascade='all, delete-orphan'
    )
    
    #ensure the category one of the following categories:
    #"strength", "cardio", "flexibility"
    @validates('category')
    def validate_category(self, key, category):
        acceptedCategories = ["strength", "cardio", "flexibility"]

        if category not in acceptedCategories:
            return f"The category not found. The following are the accepted categories {acceptedCategories}"

        return category
        

    #validate name
    #ensure the name is  notempty
    #ensure the name is between 3 and 20 characters
    @validates('name')
    def validate_name(self, key, name):

        #check if it is not empty
        if not name:
            return f"The name cannot be empty"
        
        #check the length of the name
        if not 3 < len(name) < 20:
            return f"The number of characters should be between 3 and 20"
        
        return name
        

#create schema for exercise model
class ExerciseSchema(Schema):

    id = fields.Integer(dump_only=True)
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()

    workouts = fields.Nested(lambda:WorkoutSchema (exclude=("exercises",)))

    #Ensure all exercise fields are not duplicated by first checking it in the db
    @validates_schema
    def validate_duplicate_exercise(self, data, **kwargs):

        existing_exercise = Exercise.query.filter_by(

            name = data["name"],
            category = data["category"],
            equipment_needed =  data["equipment_needed"]

        ).first()

        if existing_exercise:
            raise ValidationError("Exercise already exists")
        

    
class Workout(db.Model):
    
    __tablename__ = "workouts"
    

    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # Association proxy to get exercises for a workout through workout_exercises table
    exercises = association_proxy(
                    'workout_exercises', 
                    'exercise',
                    creator=lambda exercise_obj: WorkoutExercise(exercise=exercise_obj)
    )


    #define a relationship with the association table => workout_exercise.workout
    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates='workout', 
        cascade='all, delete-orphan'
    )
    
    #Ensure the date is not in the future
    @validates("date")
    def validate_date(self, key, date):
        
        #check if date is correct
        if date > date.today():
            raise("Date cannot be in future")
        
        return date

    #Ensure the duration minutes of the workout is not negative
    @validates("duration_minutes")
    def validate_duration_minutes(self, key, duration_minutes):
        
        #check if the minutes are negative
        if duration_minutes <= 0:
            raise("The duration must be positive")
        
        return duration_minutes

#create schema for the workout model
class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()

    exercises = fields.Nested(lambda:ExerciseSchema (exclude=("workouts",)))

    #Ensure all workout fields are not duplicated by first checking it in the db
    @validates_schema
    def validate_duplicate_workout(self, data, **kwargs):
        existing_workout = Workout.query.filter_by(

            date = data["date"],
            duration_minutes = data["duration_minutes"],
            notes =  data["notes"]

        ).first()

        if existing_workout:
            raise ValidationError("Workout already exists")


class WorkoutExercise(db.Model):
    
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer,primary_key=True)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    #Define foreign keys
    workout_id = db.Column(db.Integer,db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer,db.ForeignKey('exercises.id'))

    exercise = db.relationship('Exercise', back_populates= "workout_exercises")
    workout = db.relationship('Workout', back_populates= "workout_exercises")




