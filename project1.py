from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to db successful")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    return connection


connect = create_connection(
    'cis2368fall.c7cw0mymmpoj.us-east-1.rds.amazonaws.com',  
    'admin',  
    'ZlatanIbra1',  
    'cisfall2368db'  
)