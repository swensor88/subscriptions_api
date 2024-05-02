# NWO Subscriptions

##Overview

This is my submission for the inteview screening process for NWO.ai. It is a simple REST API built on Django. It is fully containerized and should be easy to install.

##Installation

### Pre-Requisites

- Docker/Docker Desktop
- python3
- Git
- GitHub Account (for cloning this repository)
- Please have Network subnet 175.40.0.0/16 available on your local Docker environment. Alternatively, you can change these values in docker-compose.yml

### Step 1: Clone repository

Run this command to clone the repo on your local machine
```bash
git clone https://github.com/swensor88/nwo_subscriptions_demo.git
```

### Step 2: Make your .env File

Easiest method is to copy example file, using this command:
```bash
cp nwo_subscriptions/subscriptions/subscription_api/.env.example nwo_subscriptions/subscriptions/subscription_api/.env
```

### Step 3: Build With Docker Compose

Enter the project's root folder: 

```bash
cd nwo_subscriptions
```

Run this command to build images for the db and the api

```bash
docker-compose build
```


### Step 4: Update/Start Container

Run this command to update and start your containers in detached mode.
```bash
docker-compose up -d
```

Note: If the API has any issues connecting the database, try to start it again manually.