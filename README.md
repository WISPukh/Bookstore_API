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

## Prod.by

+ [Boyushenko Aleksandr :shipit: :call_me_hand: :man_technologist:](https://t.me/SandrSX)

+ [Puchov Oleg :trollface: :exploding_head: :octocat:](https://t.me/JustFinn363)
