from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

#Define routes and endpoints

@app.route("/", methods=["GET"])
def index():
    body = {"msg": "welcome to the workout platform"}
    make_response(body,200)

#Perform CRUD operations to /workouts resource

# READ => GET /workouts resource
@app.route("/workouts", methods=["GET"])
def get_all_workouts():
    workouts = []

    for workout in Workout.query.all():
        workout_dict = {
            "id": workout.id,
            "date": workout.date,
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }
        workouts.append(workout_dict)
    
    body = {
        "workouts": workouts
    }

    # Serialize the body back to JSON
    _body = WorkoutSchema().dump(body)

    return make_response(_body, 200)

# READ => GET specific /workouts resource
@app.route("/workouts/<id>", methods=["GET"])
def get_workout(id):

    workout = Workout.query.filter_by(id=id).first()

    if workout:
        body = {
            "id": workout.id,
            "date": workout.date,
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }
        status = 200

        # Serialize the body back to JSON
        _body = WorkoutSchema().dump(body)

        return make_response(_body, status)


    else:
        
        return make_response({"error": f"Workout of {id} not found."}, 404)

# CREATE => POST  a /workouts resource
@app.route("/workouts", methods=["POST"])
def create_workout():

    #extract and deserialize json from incoming request
    data = WorkoutSchema.load(request.get_json())

    #create an instance of new_workout from incoming data
    new_workout = Workout(
        date=data["date"], 
        duration_minutes=data["duration_minutes"], 
        notes= data["notes"]
    )

    try: #Try to add and commit new data to the db

        db.session.add(new_workout)
        db.session.commit()

        body = {
            "msg": "a new workout has been added successfully into database"
        }

        return make_response(body, 201)

    except Exception as err:
        body = {
            "error": f"There was an error inserting into the database {err}"
        }

        return make_response(body, 404)


# DELETE => DELETE a /workouts resource
@app.route("/workouts/<id>", methods=["DELETE"])
def delete_workout(id):
    
    #Look for workout in the database
    workout = Workout.query.filter_by(id=id).first()

    #check if workout with a specific id does not exist in the database
    if not workout:
        return make_response({{"Error": f"Workout with id:{id} cannot be found"}, 404})
    
    #What happens when the workout exists in the database
    try:
        db.session.delete(workout)
        db.session.commit()

        return make_response(
            {
            "msg": f"Workout deleted successfully",
            "workout": {}
            }, 200
        )
    
    except Exception as err:
        return make_response({"error": f"Could not delete workout: {err}"},404)

    

#Perform CRUD operations to /exercises resource

# READ => GET /exercises resource
@app.route("/exercises", methods=["GET"])
def get_all_exercises():
    exercises = []

    for exercise in Exercise.query.all():
        exercise_dict = {
            "id": exercise.id,
            "name": exercise.id,
            "category": exercise.category,
            "notes": exercise.notes
        }
        exercises.append(exercise_dict)
    
    body = {
        "exercises": exercises
    }

    # Serialize the body back to JSON
    _body = ExerciseSchema().dump(body)

    return make_response(_body, 200)

# READ => GET a /exercises resource
@app.route("/exercises/<id>", methods=["GET"])
def get_exercise(id):

    exercise = Exercise.query.filter_by(id=id).first()

    if exercise:
        body = {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        }
        status = 200

        # Serialize the body back to JSON
        _body = ExerciseSchema().dump(body)

        return make_response(_body, status)
    else:
       
        return make_response({"error": f"Exercise of id {id} not found."}, 404)

# CREATE => POST a /exercises resource
@app.route("/exercises", methods=["POST"])
def create_exercise():
     #extract and deserialize json from incoming request
    data = ExerciseSchema.load(request.get_json())

    #create an instance of new_workout from incoming data
    new_exercise = Workout(
        name=data["name"], 
        category=data["category"], 
        equipment_needed= data["equipment_needed"]
    )

    try: #Try to add and commit new data to the db

        db.session.add(new_exercise)
        db.session.commit()

        body = {
            "msg": "a new exercise has been added successfully into database"
        }

        return make_response(body, 201)

    except Exception as err:
        body = {
            "error": f"There was an error inserting into the database {err}"
        }

        return make_response(body, 404)

# DELETE => DELETE a /exercises resource
@app.route("/exercises/<id>", methods=["DELETE"])
def delete_exercise(id):
    #Look for exercise in the database
    exercise = Exercise.query.filter_by(id=id).first()

    #check if exercise with a specific id does not exist in the database
    if not exercise:
        return make_response({{"Error": f"exercise with id:{id} cannot be found"}, 404})
    
    #What happens when the exercise exists in the database
    try:
        db.session.delete(exercise)
        db.session.commit()

        return make_response(
            {
            "msg": f"exercise deleted successfully",
            "exercise": {}
            }, 200
        )
    
    except Exception as err:
        return make_response({"error": f"Could not delete exercise: {err}"},404)

# POST => CREATE on /workout_exercises endpoint by adding an exercise to a workout
@app.route("/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises", methods=["DELETE"])
def add_exercise_to_workout(workout_id, exercise_id):

    workout = Workout.query.filter_by(id=workout_id).first()
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    #Ensure workout and exercise objects exist in the db
    if not workout or not exercise:
        return make_response({"message": "Task or Volunteer was not found!"},404)
    
    #Do the following if the workout and exercise objects exist in the db
    try:
        workout.exercise.append(exercise)
        db.session.add(workout)
        db.session.commit()
        return make_response({"message": "Exercise assigned to a workout successfully!"}, 201)

    except Exception as e:
        return {"message": f"An error occurred while assigning an exercise to a workout!: {e}"}, 500


#Auto-run flask app with "python app.py" command
if __name__ == '__main__':
    app.run(port=5555, debug=True)