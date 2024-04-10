case $1 in
    "run")
        docker compose run -p 9090:9090 marketsvc
        ;;
    "customers")
        curl http://localhost:9090/api/customers
        ;;
    "custorders")
        curl http://localhost:9090/api/orders?cust_id=${2:-1}
        ;;
    "ordertotal")
        curl http://localhost:9090/api/order_total?order_id=${2:-1}
        ;;
    "ordersbet")
        curl "http://localhost:9090/api/orders_between_dates?after=2024-03-14&before=2024-03-22"
        ;;
    "neworder")
        curl -H "Content-Type: application/json" -d '{"customer_id":1,"items":[{"id":2,"quantity":4},{"id":3,"quantity":6}]}' http://localhost:9090/api/add_new_order
        ;;
    *)
        echo "unknown cmd: I know [run, customers, custorders, ordertotal, ordersbet, neworder, orderstotal]"
esac
