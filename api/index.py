from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Vercel! CRM is alive!"

@app.route('/test')
def test():
    return {"status": "ok", "message": "Vercel is working!"}