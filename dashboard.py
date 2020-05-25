import os
import sys
from test import main 
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to your Options-Trading Dashboard!'

@app.route('/update')
def update_parser():
    print("Parsing Last Week's Data...")
    main()
    return 'Update Success!'


