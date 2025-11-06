from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row  
    return conn

@app.route("/")
def index():
    return render_template("index.html")  

@app.route("/Book")
def Book():
    return render_template("Book.html")  

@app.route("/login")
def login():
    return render_template("login.html")  


@app.route("/AboutUs")
def AboutUs():
    conn = get_db_connection()
    hairdressor = conn.execute('SELECT * FROM hairdressor').fetchall()
    conn.close()
    return render_template("AboutUs.html", hairdressor=hairdressor)  

@app.route('/products')
def Products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM PRODUCTS').fetchall()
    conn.close()

    image_map = {
        'MShampoo': 'Shampoo.jpg',
        'smartyConditioner': 'Conditioner.jpg',
        'M011TGel': 'Hair gel.jpg',
        'HSerum': 'Hair serum.jpg',
        'fabHairBrush': 'Hair brush.jpg',
        'LAORIVHairMask': 'Hair mask.jpg'
    }
    return render_template('products.html', products=products, image_map=image_map)

@app.route('/services')
def Services():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    conn.close()

    service_images = {
        'WomanTrim': "Womans' Trim.jpg",
        'WomanCut': "Womans' Cut.jpg",
        'MenCut': "Mens' cut.webp",
        'Balayage': 'Balayage.jpg',
        'Highlights': 'Highlights.jpg',
        'Semi-permanent colour': 'Semi-permanent colour.webp',
        'Toner': 'Toner.webp',
        'Lowlights': 'Lowlights.jpg',
        'Permanent colour': 'permanent colour.jpg'
    }
    return render_template('services.html', services=services, service_images=service_images)

if __name__ == "__main__":
    app.run(debug=True)
