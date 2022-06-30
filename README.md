# E-Assessment

Learning and Assessment Plattform for RA.

## Foldersturcture

- EAss: E-Assessment App
- LAna: Learning Analytics App
- EAssLAna: Server config

-> Accessing the E-Assessment-Part: http://127.0.0.1:8000/eassessments

-> Accessing the Learning-Analytics-Part: http://127.0.0.1:8000/learninganalytics

## Requriements

1. Python 3.4+
2. Python-pip3

## Running the server

1. Active the venv as uswell
2. Change the directory to EAssLAna
3. Migrate the database if needed
4. Install missing dependencies if needed
5. Run the django server
6. Go to http://127.0.0.1:8000/

Migrate the database (STEP 3.):
```
python manage.py migrate
```

Install missing dependencies (STEP 4.):
```
pip install -r requirements.txt 
```

Run the following django commands (STEP 5.):
```
python manage.py runserver
```

## Setup 

1. Setup/initalize a virtual environment (venv)
2. Active the virtual environment
3. Install missing dependencies if needed

Intialize the venv
```
python3 -m venv .env
```

Active the venv on Windows:
```
.env\Scripts\activate.bat
```

Active the venv on Linux/Unix:
```
source .env/bin/activate
```

Install missing dependencies:
```
pip install -r requirements.txt 
```
