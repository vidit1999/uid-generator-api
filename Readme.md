# Unique UID Generator API
Unique `64` bit UID Generator API created using FastAPI.
> Components of UID
* `time ms` -> `40` bits
* `process id` -> `4` bits
* `thread id` -> `8` bits
* `counter` -> `12` bits


## Setup
Run the following commands in terminal,
```
$ python -m venv venv
$ source venv/Scripts/activate
(venv) $ pip install -r requirements.txt
(venv) $ python main.py
```

## Server Access
* You can open `http://127.0.0.1:8000/docs` in browser to access Swagger UI. Sample curl,
```
curl -X 'GET' \
  'http://127.0.0.1:8000/get-uid-batch?batch-size=5' \
  -H 'accept: application/json'
```
