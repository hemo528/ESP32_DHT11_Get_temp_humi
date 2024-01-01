from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql.cursors
import logging

app = Flask(__name__)
CORS(app, origins='http://192.168.31.18')  # 允许指定来源的跨域请求

# MySQL configuration
mysql_config = {
    'host': '192.168.31.99',
    'user': 'hemo',
    'password': '1982737177',
    'database': 'userdata',
    'port': 3306,
}

# 设置日志级别为 DEBUG
app.logger.setLevel(logging.DEBUG)

# API endpoint to fetch data
@app.route('/api/fetch-data', methods=['GET'])
def fetch_data():
    app.logger.info(f"Received request from {request.remote_addr}")

    # 打印数据库连接信息
    app.logger.debug(f"Connecting to MySQL: {mysql_config}")

    connection = pymysql.connect(**mysql_config)

    try:
        with connection.cursor() as cursor:
            query = 'SELECT * FROM temp_moisture ORDER BY time'
            cursor.execute(query)
            results = cursor.fetchall()
    except Exception as e:
        app.logger.error('Error executing query:', e)
        return jsonify(error='Internal Server Error'), 500
    finally:
        connection.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
