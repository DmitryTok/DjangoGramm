![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-3760A9?style=for-the-badge&logo=python&logoColor=white)
![Makefile](https://img.shields.io/badge/Makefile-FF0033?style=for-the-badge&logo=gnu%20make&)
![Flake8](https://img.shields.io/badge/Flake8-FFA500?style=for-the-badge&logo=python&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-FAB040?style=for-the-badge&logo=pre-commit&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-4285F4?style=for-the-badge&logo=cloudinary&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Ajax](https://img.shields.io/badge/Ajax-1572B6?style=for-the-badge&logo=ajax&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)


## To run the project

#### Create and feel the .env file
```
DB_ENGINE=<...> # specify that we work with postgresql data base
DB_NAME=<...> # data base name
DB_USER=<...> # login for connecting to data base
DB_PASSWORD=<...> # password for connection to data base (create your own)
DB_HOST=<...> # name of the servise (container)
DB_PORT=<...> # port for conection to data base
SECRET_KEY=<...> # set up SECRET_KEY for django project
GET_EMAIL_HOST_USER=<...> # specify email address for sending emails
GET_EMAIL_HOST_PASSWORD=<...> # specify special code from your email system
TEST_DB_NAME=<..> # specify that we work with postgresql test data base
```

#### Create a superuser
```commandline
make superuser
```
#### After superuser run container
```commandline
make run
```
#### To stop container
```commandline
make stop
```

#### To create a webpack for JS
```commandline
npm run build
```

#### To run a webpack
```commandline
npm start
```

## Server will be available at this address: http://localhost:8000/