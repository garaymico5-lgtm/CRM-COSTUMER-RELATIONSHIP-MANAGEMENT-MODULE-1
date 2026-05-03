from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World! Vercel is working!"

@app.route('/login')
def login():
    return "Login page - working!"