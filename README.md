# SQLAlchemy Workshop

## No More Raw SQL: SQLAlchemy, ORMs and asyncio

This repository contains the code for the Marketplace service demo to follow along the **No More Raw SQL: SQLAlchemy, ORMs and asyncio workshop**. 

#### Please use this link for the workshop tutorial itself: [SQLAlchemy Workshop](https://aelsayed95.github.io/sqlalchemy-wkshop/)

### How to run this service?

1. Build the Docker containers
    ```console
    docker compose build
    ```

2. In one terminal window, run
    ```console
    docker compose run -p 9090:9090 marketsvc
    ```

3. Once the service is running, you can interact with it over http using `curl`. We’ve created a simple shell script to make it easier for you to do so. For example,
    ```console
    ./run.sh ordertotal 2
    ```
    which is equivalent to
    ```console
    curl http://localhost:9090/api/order_total?order_id=2
    ```
