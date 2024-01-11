# VELOX WEBAPP

## Local development

main folder for web application is in folder `velox_webapp`

### Set up Python

we're using Python 3.9 so if system allows you to download and install... If you have 3.7 that should work for start as
well.  
other option is to use tool PyEnv to install concrete version Installation procedure is
here [https://github.com/pyenv/pyenv#installation](https://github.com/pyenv/pyenv#installation)

Good habit is to use [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html). This allows handling isoleted
Python interpreters (so for example different versions of the same library don't clashed if used in various projects)   
On the url are steps to install and setup

to install extra libraries go to `velox_backend` and run in shell command:  
`pip install -r requirements.txt`  
this will install dependencies from the file

### PostgreSQL

- install PostgreSQL, we're using 13 if you don't have.  
- login to postgres shell `psql`
- create database  
  `CREATE DATABASE velox_db_dev;`
- create user
  `CREATE USER velox_dev with encrypted password 'velox_dev';`
- add privileges    
  `GRANT ALL PRIVILEGES ON DATABASE velox_db_dev to velox_dev;`

### Make migrations

go to folder `velox_backend` and run command:  
`python manage.py migrate` or just `./manage.py migrate`
if everything was ok (namely DB access set correctly) it should create tables

### Create Superuser

`python manage.py createsuperuser` this will prompt you for email, password etc, write whatever suits you, since this is
for local DB.

### Run local server

`python manage.py runserver` this starts local server on `localhost:8000`

### Login to Admin area

[http://localhost:8000/admin/](http://localhost:8000/admin/)
you use credentials which you entered for Superuser. This is Admin area, here are models (tables) and you can easily
create some (Horse, Measurement).  
Admin area is great that you can create dummy data very quickly or check content of a database.

### Access static files

Static files are located in
folder [velox_backend/velox_app/static/velox](velox_webapp/velox_backend/velox_app/static/velox/)
here you can add your (static) files: images, javascript, CSS etc.

URL for static files is in path starting [http://localhost:8000/static/velox/](http://localhost:8000/static/velox/)  
for example [http://localhost:8000/static/velox/js/main.js](http://localhost:8000/static/velox/js/main.js)

At the moment `main.js` file (Vue.JS app) is served from the html
file [vue_index.html](velox_webapp/velox_backend/velox/templates/vue_index.html)

On Google Cloud, static files are copied to Cloud Storage Bucket during deployment
`velox_webapp_static` is for prod, and I created `velox-webapp-static-dev` for dev/testing

Google Cloud Storage is caching files, so I'm adding timestamp after filename to prevent (that's just temporary). I'll
add preprocessing so server automatically generates hashes (based on file content) during deployment

### Frontend

(keep in mind that Frontend/Javascript is not my strong side)

I am running script [build.sh](velox_webapp/velox_frontend/build.sh) which builds project and copy file to static
folder.  
With the current setup it counts that Vue JS will handle all the routing.

I'm leaving up to you how to organize velox_frontend folder, and it's content, build etc.

### Backend and APIs

Database models (tables) are defined in file [models.py](velox_webapp/velox_backend/velox_app/models.py), so far we have
two main models: Horse and Measurement.

Django RESTfull is the framework I am using to expose models to APIs.

APIs are starting at these urls: [http://localhost:8000/velox/api/](http://localhost:8000/velox/api/)  
The most import are:

- [http://localhost:8000/velox/api/horses/](http://localhost:8000/velox/api/horses/)
- [http://localhost:8000/velox/api/measures/](http://localhost:8000/velox/api/measures/)
- [http://localhost:8000/velox/api/users/](http://localhost:8000/velox/api/users/)
- [http://localhost:8000/velox/api/users/login](http://localhost:8000/velox/api/users/login)
- [http://localhost:8000/velox/api/users/logout](http://localhost:8000/velox/api/users/logout)

You can do basic CRUD operation

"interface" input/outputs (fields) are defined
through [serializers](velox_webapp/velox_backend/velox_app/serializers.py)
and views (handling requests) are in [views_api.py](/velox_webapp/velox_backend/velox_app/views_api.py). Since most
stuff is done by framework, here is just some custom code and minimal settings.  

#### Authentication
Every user has Token. When user logs in, in response is returned token that should be used with every other request.    
**Token** is set in **Authorization** header in format:  
Authorization: Token <token_value>


#### Filtering

API supports filtering for Horse currently on following fields: 'elite', 'country', 'status', 'active'    
`/velox/api/horses/?elite=Yes&country=Europe`  

#### Ordering 
`/velox/api/horses/?ordering=country`  
for descending ordering use '-' prefix before field name  
`/velox/api/horses/?ordering=-country`  

#### Page Size
use parameter 'page_size'  
`/velox/api/horses/?page_size=25`  

#### Search
at the moment search is supported for Horse name:
`/velox/api/horses/?search=Molly`  

#### Uploading of videos

There are specific steps for video upload, since we're not doing it through server but write content straight to bucket.
When user submits form to create Measure (and select files):

- API [/velox/api/upload/get_signed_url/](/velox/api/upload/get_signed_url/) is called with parameters:
    - filename - the name of the file that is being uploaded
    - content_type - content type of the file
    - video_type. if it's cardio, set 'cardio' otherwise it's not important (for now)
    - date_of_measure - format YYYY-MM-DD, i.e 2022-01-17 API then returns url to which content of the file is uploaded.

You can see how I implement it (although I think perhaps it can be done little more elegant)

# Frontend
create `.env` file inside of `velox_frontend2` folder with the content  
```bash
VUE_APP_STATIC_GCS_BUCKET=http://localhost:8000/static
VUE_APP_API_URL=http://localhost:8000/velox/api/
```


# Google Cloud Setup

at the moment, application is deployed on **Cloud Run** as docker image.  
Static files are served on **Cloud Storage**  
We're using **Cloud SQL** for managed PostgreSQL DB  
**Cloud Build** for deployments

### Other folders

- [deeplabcut_time_series](deeplabcut_time_series) - processing h5 output videos to Granula Angular Field images
- [deeplabcut_webapp](deeplabcut_webapp) - Webapp/microservice which handles processing of uploaded video
- [scripts](scripts) - helpful scripts
- [vertex_pipelines](vertex_pipelines) - ML pipelines/processing  
