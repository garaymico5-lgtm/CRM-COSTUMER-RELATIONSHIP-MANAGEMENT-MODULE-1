from flask import Flask, render_template
import os

app = Flask(__name__)

# I-set ang templates folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.template_folder = os.path.join(BASE_DIR, 'templates')

@app.route('/')
def home():
    try:
        return render_template('login.html')
    except Exception as e:
        return f"Error loading template: {str(e)}"

@app.route('/test')
def test():
    return {
        "status": "ok", 
        "message": "Vercel is working!",
        "templates_folder": app.template_folder,
        "templates_exist": os.path.exists(app.template_folder)
    }

@app.route('/menu')
def menu():
    try:
        return render_template('menu.html')
    except Exception as e:
        return f"Error loading menu: {str(e)}"

@app.route('/customer-menu')
def customer_menu():
    try:
        return render_template('customer_menu.html')
    except Exception as e:
        return f"Error loading customer menu: {str(e)}"