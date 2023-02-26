## To run the project

#### Create and feel the .env file
```
DB_ENGINE=<...> # specify that we work with postgresql data base
DB_NAME=<...> # data base name
DB_USER=<...> # login for connecting to data base
DB_PASSWORD=<...> # password for connection to data base (create your own)
DB_HOST=<...> # name of the servise (container)
DB_PORT=<...> # port for conection to data base
```

#### Run container
1. docker-compose up -d db
2. docker-compose run web python manage.py makemigrations
3. docker-compose run web python manage.py migrate
4. docker-compose run web python manage.py runserver

#### Stop container with this command
docker-compose down -v
