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

#### Create a superuser
```
make superuser
```
#### After superuser run container
```
make up
```

## Server will be available at this address: http://localhost:8000/