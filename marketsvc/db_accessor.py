import logging
import os

import asyncpg

DB_CONFIG = {
    "database": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "host": os.environ.get("POSTGRES_DB"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "port": os.environ.get("POSTGRES_PORT"),
}


async def execute_query(query, *params):
    conn = await asyncpg.connect(**DB_CONFIG)
    async with conn.transaction():
        return await conn.fetch(query, *params)


async def stream_query(query, *params):
    conn = await asyncpg.connect(**DB_CONFIG)
    async with conn.transaction():
        async for row in conn.cursor(query, *params):
            yield row


async def execute_insert_query(query, params):
    conn = await asyncpg.connect(**DB_CONFIG)
    async with conn.transaction():
        result = conn.cursor(query, params)
        return result


def get_customers():
    rows = stream_query("SELECT * FROM customer")
    return rows


async def get_orders_of_customer(customer_id):
    rows = await execute_query(
        """
        SELECT 
            item.name, 
            item.description, 
            item.price, 
            item.price*order_items.quantity
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item
        ON 
            item.id = order_items.item_id
        WHERE
            orders.customer_id=$1
        """,
        customer_id,
    )
    return rows


async def get_total_cost_of_an_order(order_id):
    rows = await execute_query(
        """
        SELECT 
            SUM(item.price*order_items.quantity)
        FROM orders 
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.id=$1
        """,
        order_id,
    )
    return rows[0].get("sum")


def get_orders_between_dates(after, before):
    rows = stream_query(
        """
        SELECT
            customer.name,
            item.name, 
            item.price, 
            item.price*order_items.quantity
        FROM orders 
        JOIN customer
        ON
            customer.id = orders.customer_id
        JOIN order_items 
        ON 
            order_items.order_id = orders.id 
        JOIN item 
        ON 
            item.id = order_items.item_id
        WHERE
            orders.order_time >= $1
        AND
            orders.order_time <= $2
        """,
        after,
        before,
    )
    return rows


async def add_new_order_for_customer(customer_id, items):
    try:
        new_order_id = await execute_insert_query(
            """
            INSERT INTO orders
                (customer_id, order_time)
            VALUES
                ($1, NOW())
            RETURNING id
            """,
            customer_id,
        )

        (
            await execute_insert_query(
                """
            INSERT INTO order_items
                (order_id, item_id, quantity)
            VALUES ($1, $2, $3)
            """,
                (
                    (new_order_id, item["id"], item["quantity"])
                    for item in items
                ),
            )
        )
        return True

    except Exception:
        logging.exception("Failed to update order")
        return False
