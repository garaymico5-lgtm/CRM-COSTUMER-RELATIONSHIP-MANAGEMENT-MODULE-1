from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Vercel! CRM is working!"

@app.route('/test')
def test():
    return {"status": "ok", "message": "Vercel is working with Python 3.12!"}