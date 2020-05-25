import os
import sys
import mysql.connector
from flask import Flask

from dbconfig import mysql
from parser import main 

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to your Options-Trading Dashboard!'

@app.route('/update', methods=['POST'])
def update_parser():
    print("Parsing Last Week's Data...")
    main()
    return 'Update Success!'

@app.route('/stocks', methods=['GET'])
def retrieve_stocks():
    # TODO: add logic to process stock data and return response
    return 'PLACEHOLDER'
