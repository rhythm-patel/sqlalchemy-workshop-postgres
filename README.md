# SQLAlchemy Workshop

## No More Raw SQL: SQLAlchemy, ORMs and asyncio

This repository contains the code for the Marketplace service demo to follow along the **No More Raw SQL: SQLAlchemy, ORMs and asyncio workshop**. 

Please use this link for the workshop tutorial itself: [SQLAlchemy Workshop](https://aelsayed95.github.io/sqlalchemy-wkshop/)

### How to run this service?

1. Build the Docker containers
    ```
    docker compose build
    ```

2. In one terminal window, run
    ```
    ./run.sh run
    ```
    OR
    ```console
    docker compose run -p 9090:9090 marketsvc
    ```

3. Once the service is running, run the `curl` commands you require in another terminal window, such as
    ```console
    ./run.sh customers
    ```
