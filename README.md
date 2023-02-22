## To run the project

#### Create and feel the .env file
```
ENGINE=<...> # specify that we work with postgresql data base
NAME=<...> # data base name
USER=<...> # login for connecting to data base
PASSWORD=<...> # password for connection to data base (create your own)
HOST=<...> # name of the servise (container)
PORT=<...> # port for conection to data base
```

#### Run container
1. docker-compose up -d --build --force-recreate
2. python3 manage.py makemigrations
3. python3 manage.py migrate
4. python3 manage.py runserver

#### Stop container with this command
docker-compose down -v
