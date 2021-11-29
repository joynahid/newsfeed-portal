# News Portal 

- [News Portal](#news-portal)
  - [Installation](#installation)
  - [Usage](#usage)

## Installation

Only tested on Ubuntu 20.04 LTS and 5.10.0-kali7-amd64. Might work in other linux distributions (Docker Magic).

You will need **docker and docker-compose** installed to spin up this app in seconds. If you do not have these installed please install it from [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

You need to create two free accounts in Sendgrid and NewsAPI beforehand.
- Sendgrid ( https://sendgrid.com/ ) - For sending emails
- NewsAPI ( https://newsapi.org/ ) - For fetching news

Grab those APIs and put it inside your `.env` file. Also fill in the variables in `.env copy` file and save it as exactly `.env` These configs are important!

Now fire up your terminal.

Note: **Use `sudo` if necessary.**

```bash
git clone https://github.com/joynahid/newsfeed-portal.git

cd newsfeed-portal

# Config your .env file
# After that only for the first time you need to run a script file
# It will populate the required initial database
chmod +x run.sh
./run.sh

# You're done installing the app

# From now on you can spin it up
docker-compose up

# You can kill it by
docker-compose down
```

If you want to access the database and see it in action. Create a django superuser via following commands:

```bash
# Make sure the project is up and running
docker exec -it djangoapp bash

# You are inside the docker, now run and follow django's instruction
python manage.py createsuperuser
```

Trying to do manual installation? Great! You can follow the scripts, `Dockerfile` and `docker-compose.yml` file. Good luck!


## Usage
You can use [this POSTMAN FILE](files/News%20Portal.postman_collection.json) to have a quick look what are the available API endpoints. Remeber to add a postman variable `base_url` in the environment. You can login and acquire the token and set to the collection/global header for accessing portected endpoints.

There is a very simple web user interface that you can access by visiting [http://localhost:8000](http://localhost:8000) (Keep you docker container running)
- Create an account
- Login into that account
- Set up your preference in settings
  - Add keywords separated by commas to get email notification (Keep your email valid during registration)
- See your feed at Newsfeed