from app import app
from models import *
import datetime

with app.app_context():

	# reset data and add new example data, committing to db
    Workout.query.delete()
    WorkoutExercise.query.delete()

    db.session.commit()

    #Populate data to the database

    #exercises
    ex1 = Exercise(name="push ups" , category="strength" , equipment_needed=False)
    ex2 = Exercise(name="weight lifting" , category="cardio" , equipment_needed=True)
    ex3 = Exercise(name="squats" , category="cardio" , equipment_needed=False)
    ex4 = Exercise(name="rope skipping" , category="flexibility" , equipment_needed=True)

    #workouts
    wo1 = Workout(date= datetime.datetime(2022, 5, 17) , duration_minutes= 5 , notes="fantastic! will try again")
    wo2 = Workout(date= datetime.datetime(2024, 9, 11) , duration_minutes= 15 , notes="fantastic! will try again")
    wo3 = Workout(date= datetime.datetime(2022, 12, 17) , duration_minutes= 5 , notes="fantastic! will try again")

    # Add workouts to exercises
    ex1.workouts.append(wo1)
    ex1.workouts.append(wo3)

    # Add exercises to workouts
    wo2.exercises.append(ex2)
    wo2.exercises.append(ex3)
    wo2.exercises.append(ex4)

    woex1 = WorkoutExercise(
        reps=2,
        sets=25,
        duration_seconds=300,
        exercise=ex1,
        workout=wo1,
    )

    woex2 = WorkoutExercise(
        reps=7,
        sets=20,
        duration_seconds=480,
        exercise=ex2,
        workout=wo1,
    )

    woex3 = WorkoutExercise(
        reps=5,
        sets=18,
        duration_seconds=160,
        exercise=ex2,
        workout=wo2,
    )
    
    



    
    


