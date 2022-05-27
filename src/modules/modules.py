from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='../templates' , static_folder='../static')
mysql = MySQL(app)
