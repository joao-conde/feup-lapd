Some extra routes to retrieve information that extends the database's original "schema".

## How to run
It is configured as a docker service (just like, e.g., the database), so running `docker-compose up -d` from the root directory starts this service. To start only this service, run `docker-compose up extra_api`. To rebuild & run, run `docker-compose up --build extra_api`. Base endpoint will be localhost:5050

## What are the endpoints available?
Access the root server page (localhost:5050/), which will show a list of the available routes
