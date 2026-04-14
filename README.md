# Flask SQLAlchemy Workout Application Backend Project

This is a python Flask-based backend application that demonstrates a many-to-many relationship between exercises and workouts. An exercise can be linked to multiple workouts and a single workout can be linked to multiple exercises. 

Exercise and workout are represented as object models to retrieve, modify and store data in the database. It also includes endpoints which help a front-end application to interact with an API data. This API data is validated at both the database level and schema level to enable correct serialization and deserialization.

The following are ways you can interact with the Workout Application Backend API which is implemented by an SQLITE engine.

- **Retrieving all workouts from the database**
```bash
GET /workouts #get all workouts
GET /exercises #get all exercises
```

- **Retrieving a particular workout/exercise from the database**. Specify the **id** of the workout item you want t o retrieve
```bash
GET /workouts/{id} # retrieve a workout
GET /exercises/{id} # retrieve an exercise
```

- **Create a particular workout/exercise in the database**. Specify the **id** of the workoutexercise item you want to create in the database.
```bash
workout_payload = {
    "date": <Date>
    "duration_minutes": <Integer>
    "notes": <Text>
}

exercise_payload = {
    "name": <String>,
    "category": <String>,
    "equipment_needed": <Boolean>

}
```
```bash
POST /workouts/{id} #workout
POST /exercises/{id} #exercise
```

- **Delete a particular workout/exercise in the database**. Specify the **id** of the workoutexercise item you want to delete from the database.
```bash
DELETE /workouts/{id} #workout
DELETE /exercises/{id} #exercise
```

## Prerequisites
Ensure you have installed Python in your machine:

```bash
python --version
```

**Optional**:Create and activate the Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
```

Fork [this repository](https://github.com/joshua-odero/flask-sqlalchemy-workout-application-backend.git) , then clone it to your preferred destination with the following command:

```bash
git clone <your SSH/Http path>
```

## Installing dependencies
Switch to the app directory using the **cd** command, Use the **pip** to install the core project dependencies from pypi like :
- **Flask** which is the main framework for the web app development in python
- **Flask Migrate** for database version control without losing crucial data
- **Marshmallow** which adds a layer of data integrity to the database by validating incoming data and data from the Flask application

```bash
cd flask-sqlalchemy-workout-application-backend
```

```bash
pip install <package_name>
```
or 

[Use the packages in the Pipfile](./Pipfile) to install all packages in the virtual environment:
```bash
pipenv install
```
or

Use Pip to install python packages:

```bash
pip install -r requirements.txt
```


## Running the project
In the project's root directory, execute the following command to run a .py script within the directory. Use **python** or **python3** commands depending on your OS:

```bash
python3 <example_file.py> #OR python3 <example_file.py>
```

### STEP 1: Run the Flask application
**NOTE:** **Run the Flask app first** to test your frontend application interaction with the application's API:

```bash
python app.py #python3 app.py
```

### STEP 2: Set up the database and create tables
To set up the database to run locally, run:

```bash
flask db init
```
Upgrade to migrate to the the latest version of the database:

```bash
flask db upgrade head
```

### STEP 3: Populate the database
Run seed.py on your terminal to populate sample data and use it to test the API's data:

```bash
python seed.py #python3 seed.py
```


