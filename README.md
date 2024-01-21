# instruction to execute the server

This server is an API for retrieving recommended restaurants. It uses a PostgreSQL database and runs within a Docker container.
Open Terminal
`pip install -r requirements.txt` for installing resources

Create Docker images from the Dockerfile specified in docker-compose.yml for every service.
`docker-compose build` 

Create and Start containers as specified in docker-compose.yml.
`docker-compose up`

Run the command in the container named app as specified in the file. docker-compose.yml. and commands run in the container, here using Alembic to create a migration file
`docker-compose run app alembic revision --autogenerate -m "New Migration"`

Upgrade the database using Alembic to the latest version (head).
`docker-compose run app alembic upgrade head`

Connect the database with pgAdmin and Add information to the database
Add data user and restaurants on container
`docker cp /path/file.csv CONTAINER ID:/path/in/container/file.csv'`

Add data to the database using SQL commands.
`**COPY your_table FROM '/path/in/container/file.csv' WITH CSV HEADER;**`

Run Api on post `:8000`
Run Test on post `:8089`
