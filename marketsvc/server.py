import asyncio
import os

from db_accessor import (
    add_new_order_for_customer,
    get_customers,
    get_orders_between_dates,
    get_orders_of_customer,
    get_total_cost_of_an_order,
)
from flask import Flask, Response, jsonify, request
from formatters import str_to_date

app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Welcome to MarketPlace!</h1>"


@app.route("/api/customers")
async def customers():
    customers = get_customers()
    response = [customer._asdict() async for customer in customers]
    return jsonify(response)


@app.route("/api/orders")
async def orders():
    cust_id = int(request.args.get("cust_id"))
    orders = await get_orders_of_customer(cust_id)
    response = [order._asdict() for order in orders]
    return jsonify(response)


@app.route("/api/order_total")
async def order_total():
    order_id = int(request.args.get("order_id"))
    total_cost = await get_total_cost_of_an_order(order_id)
    return jsonify({"total_cost": total_cost})


@app.route("/api/orders_total")
async def orders_total():
    orders = request.json.get("orders", [])
    async with asyncio.TaskGroup() as tg:
        order_tasks = [
            tg.create_task(get_total_cost_of_an_order(order))
            for order in orders
        ]
    return jsonify([task.result() for task in order_tasks])


@app.route("/api/orders_between_dates")
async def orders_between_dates():
    after = str_to_date(request.args.get("after"))
    before = str_to_date(request.args.get("before"))
    orders = get_orders_between_dates(after, before)
    response = [order._asdict() async for order in orders]
    return jsonify(response)


@app.route("/api/add_new_order", methods=["POST"])
async def add_order_items():
    customer_id = request.json.get("customer_id")
    items = request.json.get("items")

    success = await add_new_order_for_customer(customer_id, items)
    return Response(status=200) if success else Response(status=500)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=os.environ.get("FLASK_SERVER_PORT", 9090),
        debug=True,
    )
