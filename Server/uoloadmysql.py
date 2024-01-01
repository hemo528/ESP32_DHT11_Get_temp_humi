from flask import Flask, request
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)

# MySQL配置
app.config['MYSQL_HOST'] = '192.168.31.99'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'hemo'
app.config['MYSQL_PASSWORD'] = '1982737177'
app.config['MYSQL_DB'] = 'userdata'

mysql = MySQL(app)

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.json
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp = float(data['temp'])
    moisture = float(data['moisture'][:-2])

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO temp_moisture (time, temp, moisture) VALUES (%s, %s, %s)", (time, temp, moisture))
    mysql.connection.commit()
    cur.close()

    return 'Data received and stored successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
