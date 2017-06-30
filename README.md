### I created a Postgres in AWS for testing, so you just want to run service and test.

Run service
```
$ cd root_path
$ virtualenv -p python3.6 .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python main.py
```

How to use:
```
# Create shorten URL
$ curl -X POST -F url="http://youtube.com" http://localhost:9999/url
{
  "shorten_url": "http://lin.ks/jR"
}
# And when user go to http://lin.ks/<hashid> forward hashid to server
$ curl -X GET http://localhost:9999/url/jR
{
  "url": "http://youtube.com"
}
```

### My DB host have very low RAM so it may be slow, you can run your own DB

Run PostgreSQL
```
$ docker run --name postgres-deps -e POSTGRES_USER=<user> -e POSTGRES_PASSWORD=<passwd> -e POSTGRES_DB=<db_name> -p 5432:5432 -d postgres
```

Run Alembic to migrate
```
$ cd root_project/
$ env PYTHONPATH=. POSTGRES_USER=<user> POSTGRES_HOST=<host> POSTGRES_PASSWD=<passwd> POSTGRES_DB=<db_name> alembic -c conf/alembic.ini upgrade head
```

Run service
```
$ virtualenv -p python3.6 .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ env PYTHONPATH=. POSTGRES_USER=<user> POSTGRES_HOST=<host> POSTGRES_PASSWD=<passwd> POSTGRES_DB=<db_name> python main.py
```


P/S: Just writing some doctests for lib, another function have no tests (for now)