import sqlite3
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")
DB = "flights.db"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/flights/search")
def search_flights():
    # 1. 读取网页传来的条件：出发城市、到达城市、日期、排序方式
    dep = request.args.get("from", "").strip()
    arr = request.args.get("to", "").strip()
    date = request.args.get("date", "").strip()
    sort = request.args.get("sort", "price")

    # 2. 先检查条件合不合理（没填就报错，告诉网页）
    if not dep or not arr:
        return jsonify({"code": 400, "msg": "请提供出发城市和到达城市"}), 400
    if dep == arr:
        return jsonify({"code": 400, "msg": "出发城市与到达城市不能相同"}), 400

    # 3. 拼一句话去问数据库：找 出发=dep 且 到达=arr 且 日期=date 的航班
    sql = """SELECT flight_no, airline, dep_city, dep_airport, arr_city,
                    arr_airport, dep_time, arr_time, duration, price, seats_left
             FROM flights
             WHERE dep_city = ? AND arr_city = ? AND dep_time LIKE ?"""
    params = [dep, arr, date + "%"]

    # 4. 决定按什么排：价格 或 起飞时间
    if sort == "time":
        sql += " ORDER BY dep_time ASC"
    else:
        sql += " ORDER BY price ASC"

    # 5. 真的去查数据库
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()

    # 6. 把结果打包成 JSON（一种网页能读的数据格式）送回去
    return jsonify({"code": 0, "count": len(rows), "flights": rows})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
