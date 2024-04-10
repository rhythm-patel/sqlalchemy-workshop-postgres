import os

from db_accessor import (
    add_new_order_for_customer,
    get_customers,
    get_orders_between_dates,
    get_orders_of_customer,
    get_total_cost_of_an_order,
)
from flask import Flask, Response, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Welcome to MarketPlace!</h1>"


@app.route("/api/customers")
def customers():
    customers = get_customers()
    response = [customer.as_dict() for customer in customers]
    return jsonify(response)


@app.route("/api/orders")
def orders():
    cust_id = request.args.get("cust_id")
    orders = get_orders_of_customer(cust_id)
    response = [order.as_dict() for order in orders]
    return jsonify(response)


@app.route("/api/order_total")
def order_total():
    order_id = request.args.get("order_id")
    total_cost = get_total_cost_of_an_order(order_id)
    response = {"total_cost": total_cost}
    return jsonify(response)


@app.route("/api/orders_between_dates")
def orders_between_dates():
    after = request.args.get("after")
    before = request.args.get("before")
    orders = get_orders_between_dates(after, before)
    response = [order.as_dict() for order in orders]
    return jsonify(response)


@app.route("/api/add_new_order", methods=["POST"])
def add_new_order():
    customer_id = request.json.get("customer_id")
    items = request.json.get("items")

    success = add_new_order_for_customer(customer_id, items)
    return Response(status=200) if success else Response(status=500)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=os.environ.get("FLASK_SERVER_PORT", 9090),
        debug=True,
    )
