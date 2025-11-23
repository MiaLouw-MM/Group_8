from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
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
def products():
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


@app.route("/customer_login")
def customer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        customer = conn.execute(
            'SELECT * FROM customer WHERE customer_email = ? AND password = ?',
            (email, password)
        ).fetchone()
        conn.close()

        if customer:
            # Save customer info in session
            session['customer_id'] = customer['customer_id']
            session['customer_name'] = customer['customer_name']
            session['customer_surname'] = customer['customer_surname']
            
            image_name = customer['customer_name'].lower() + ".jpeg"
            session['customer_image'] = image_name
            
            return redirect(url_for('cutomer_homepage'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('customer_login'))
    return render_template("customer_login.html")  

@app.route("/hairdressor_login", methods=['GET', 'POST'])
def hairdressor_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        hairdresser = conn.execute(
            'SELECT * FROM hairdressor WHERE hairdressor_email = ? AND password = ?',
            (email, password)
        ).fetchone()
        conn.close()

        if hairdresser:
            # Save hairdresser info in session
            session['hairdresser_id'] = hairdresser['hairdressor_id']
            session['hairdresser_name'] = hairdresser['hairdressor_name']
            session['hairdresser_surname'] = hairdresser['hairdressor_surname']
            
            image_name = hairdresser['hairdressor_name'].lower() + ".jpeg"
            session['hairdresser_image'] = image_name
            
            return redirect(url_for('hairdresser_homepage'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('hairdressor_login'))
    return render_template("hairdressor_login.html")  

@app.route("/hairdresser_homepage")
def hairdresser_homepage():
    # User is not logged in → send them back to login page
    if 'hairdresser_id' not in session:
        return redirect(url_for('hairdressor_login'))

    return render_template(
        "hairdresser_homepage.html",
        name=session['hairdresser_name'],
        surname=session['hairdresser_surname'],
        image=session['hairdresser_image']
    )
 

@app.route("/Inventory_levels")
def Inventory_levels():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM PRODUCTS").fetchall()
    conn.close()

    # Convert from sqlite rows to list of dictionaries so JS can use them
    product_list = []
    for p in products:
        product_list.append({
            "id": p["product_id"],
            "name": p["product_name"],
            "category": p["product_category"],
            "stock": p["stock_quantity"],
            "price": p["price"]
        })

    return render_template("Inventory_levels.html", products=product_list)

@app.route("/My_Schedule")
def My_Schedule():
    return render_template("My_Schedule.html")  

@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")  

if __name__ == "__main__":
    app.run(debug=True)
