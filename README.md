![alt text](https://static.tildacdn.com/tild3561-6163-4531-b662-383539366166/WIS_LOGO_white_NEW.svg)

# Bookstore API documentation

---

## [Docker installing instruction](https://docs.docker.com/engine/install/)

---

## Getting started

###  Setup

- Clone project

```bash
git clone https://github.com/WISPukh/Bookstore_API.git
```

- Navigate to project directory

```bash
cd Bookstore_API
```

- Copy .env parameters

```bash
cp .env.example .env
```

- In order to enable JWT Authorization, edit your variable in .env file to make it look like this

```dotenv
JWT_AUTH=1
```
- To authorize, in swagger click **authorize** and type:
```Bearer <and here is your token>```

- In order to change token lifetime, edit your variable in .env file to make it look like this

```dotenv
# In hours
ACCESS_TOKEN_LIFETIME=1
REFRESH_TOKEN_LIFETIME=24
```
## IMPORTANT
If You have pulled project and changes were made on origin, to make sure that **everything** is up-to-date run this command
(deletes previous versions of images, containers, volumes and network):
```bash
make clear_docker_files
```
After that just build and run project with:
```bash
make build
make up
```
Or simply use command **_make up_** that does same thing
### Launch API

- To build and up docker containers for API run the command

```bash
make up
```

- To fill Database with test data, run the command

```bash
make fill_db
```

- To clear Database of test data, run the command

```bash
make flush_db
```

### Connection

- In order to open swagger page, follow this link

    - [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

- In order to open admin panel, follow this link

    - [http://localhost:8000/admin/](http://localhost:8000/admin/)

```text
login: admin@admin.admin
password: admin
```

- In order to open API documentation page, follow this link

     - [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---
# WINDOWS TROUBLESHOOTING 
Make commands don't work on Windows and there is no lightweight and easy to use analogy,
so here goes all docker commands that you will need:

+ Start API:
```bash
docker-compose -f docker-compose-local.yml up -d
```

+ Build or rebuild services
```bash
 docker-compose -f docker-compose-local.yml build
 ```
+ Create and start containers
```bash
docker-compose -f docker-compose-local.yml up -d
```
+ Start services
```bash 
docker-compose -f docker-compose-local.yml start
```
+ Stop services
```bash
 docker-compose -f docker-compose-local.yml stop
 ```

+ Stop and remove containers, networks, images, and volumes
```bash 
docker-compose -f docker-compose-local.yml down
```

+ Make migrations in running container
```bash
docker exec bookstore python manage.py makemigrations
```

+ Apply migrations in running container
```bash
docker exec bookstore python manage.py migrate
```

+ Fill database with test data
```bash
docker exec bookstore python manage.py create_data
```

+ Delete all test data
```bash
docker exec bookstore python manage.py delete_data
```

+ Delete images, volumes, containers, network for current project

_**yes, copy and past all of it in terminal**_
```bash
docker rm bookstore db
docker image rm bookstore_api-bookstore
docker volume rm bookstore_api_pg_data
docker network rm bookstore_api_default
docker system prune -f
```

---

## Prod.by

+ [Boyushenko Aleksandr :shipit: :call_me_hand: :man_technologist:](https://t.me/SandrSX)

+ [Pukhov Oleg :trollface: :exploding_head: :octocat:](https://t.me/JustFinn363)
