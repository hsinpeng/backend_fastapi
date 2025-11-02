# backend_fastapi
General FastAPI Server

## Build Docker Image
```shell=
docker build -t my-app .
```

## Initial the Environment
Create folders for docker compose:
```shell=
./reset.sh
```

Change the database URL:
```shell=
vim ./volumes/setting/.env.dev
```

## Run the Application
Whole system
```shell=
docker compose up
```

Database only
```shell=
docker compose -f docker-compose-postgres.yml up
```

## Stop the Application
```shell=
docker compose down -v
```