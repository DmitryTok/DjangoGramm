## To run the project

#### Create and feel the .env file
```
DB_ENGINE=example(django.db.backends.postgresql) # specify that we work with postgresql data base
DB_NAME=example(djangogramm) # data base name
DB_USER=example(dmitry_tok) # login for connecting to data base
DB_PASSWORD=example(postgres) # password for connection to data base (create your own)
DB_HOST=example(db) # name of the service (container)
DB_PORT=example(5432) # port for connection to data base
SECRET_KEY=example(django-insecure-qzb1y40)_a5q9#lf*hf_$lcbp+srju)7%(ssgj8+vc06uhw2r) # set up SECRET_KEY for django project
GET_EMAIL_HOST_USER=example(example@gmail.com) # specify email address for sending emails
GET_EMAIL_HOST_PASSWORD=example(verysecretcode) # specify special code from your email system
TEST_DB_NAME=example(test_djangogramm) # specify that we work with postgresql test data base
```

#### Create a superuser
```
make superuser
```
#### After superuser run container
```
make up
```

## Server will be available at this address: http://localhost:8000/