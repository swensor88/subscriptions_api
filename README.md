# NWO Subscriptions

## Overview

This is my submission for the inteview screening process for NWO.ai. It is a simple REST API built with Fast API. It is fully containerized and should be easy to install.

## Installation

### Pre-Requisites

- [Docker/Docker Desktop](https://www.docker.com/products/docker-desktop/)
- python3
- Git
- Optional: GitHub Account
- If you've been using Docker, you will need to free up network subnet 175.40.0.0/16. Deleting the stack using this subnet will work. Alternatively, you can change these values in docker-compose.yml. Learn more: [Networking in Docker Compose](https://docs.docker.com/compose/networking/)

### Step 1: Clone repository

Run this command to clone the repo on your local machine
```bash
git clone https://github.com/swensor88/subscriptions_api.git && cd subscriptions_api
```

### Step 2: Setup environment (optional)

Open up the cloned repo in IDE/terminal of your choosing. Make sure you're in the root folder which contains 'docker-compose.yml' and 'requirements.txt' files.


First, copy example file, using this command:
```bash
cp .env.example .env
```

Second, install venv 
```bash
pip install venv
```

Third, create/activate venv named env
```bash
python -m venv env && source env/bin/activate
```

Fourth, install using requirements file
```bash
pip install -r requirements.txt
```

Finally, test local server with uvicorn
```bash
uvicorn app.main:app --reload
```



### Step 3: Build With Docker Compose

Run this command to build images for the db and the api

```bash
docker-compose build
```

Note: It may be necessary to modify the volume path in docker-compose.yml, found on/near line 19. This can be removed entirely (sacrificing the ability to import/retrieve db dumps on the container) or replaced with a path that is writable when running docker-compose up -d


### Step 4: Update/Start Container

Run this command to update and start your containers in detached mode.
```bash
docker-compose up -d
```

Note: If the API has any issues connecting the database, try to start it again manually.

### Test API with Swagger

Navigate to http://127.0.0.1:8000 to view the API. It should redirect you to swagger path at /docs