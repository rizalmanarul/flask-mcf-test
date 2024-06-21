import datetime
from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
import requests
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mcf-test'

mysql = MySQL(app)

@app.route("/user/fetch/",methods=['GET'])
def user_data():
    data_source = 'https://reqres.in/api/users'
    
    page = request.args.get('page')
    if not page:
        return "Error page parameter not found, Please kindly input page parameter",400
    params = {
        'page':page
    }
    response = requests.get(data_source,params=params)

    result = response.json()
    datas = result.get('data')
    # print(datas)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id FROM users')
    user_ids = cursor.fetchone()
    # print((user_ids))

    for data in datas:
        if user_ids:
            if data.get('id') in user_ids:
                continue
        
        cursor.execute('INSERT INTO users (id,email,first_name,last_name,avatar,created_at,updated_at,deleted_at) VALUES (%i, %s, %s, %s, %s,   , NULL, NULL)', (data.get('id'), data.get('email'), data.get('first_name'), data.get('last_name'),data.get('avatar')))
        
    return "Success Input Data"