from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import datetime



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
def get_db_connection():
    conn = sqlite3.connect('inventory.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def generate_slots_for_date(duration_min, date_str):
    OPEN_MIN = 8*60
    CLOSE_MIN = 17*60
    latest_start = CLOSE_MIN - int(duration_min)
    slots = []
    t = OPEN_MIN
    while t <= latest_start:
        hh = t // 60
        mm = t % 60
        slots.append(f"{hh:02d}:{mm:02d}")
        t += 5
    return slots


def is_slot_available(conn, stylist_id, start_dt_str, duration_min):
    end_dt_str = (datetime.datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M:%S")
                  + datetime.timedelta(minutes=int(duration_min))).strftime("%Y-%m-%d %H:%M:%S")
    q = """
      SELECT 1 FROM bookings
      WHERE stylist_id = ?
        AND NOT (end_datetime <= ? OR start_datetime >= ?)
      LIMIT 1
    """
    
    cur = conn.execute(q, (stylist_id, start_dt_str, end_dt_str)).fetchone()
    return cur is None

@app.route("/")
def index():
    return render_template("index.html")  

@app.route("/Book", methods=['GET', 'POST'])
def Book():
    conn = get_db_connection()
    services = conn.execute("SELECT service_id, service_name, service_duration_min FROM services").fetchall()
    stylists = conn.execute("SELECT hairdressor_id AS id, hairdressor_name || ' ' || hairdressor_surname AS name FROM hairdressor").fetchall()

    if request.method == 'POST':
        service_id = request.form.get('service_id')
        stylist_id = request.form.get('stylist_id')
        date = request.form.get('date')                
        time = request.form.get('booking_time')         
        customer_email = request.form.get('customer_email') 

        start_dt = f"{date} {time}:00"
        duration_row = conn.execute("SELECT service_duration_min FROM services WHERE service_id = ?", (service_id,)).fetchone()
        duration_min = int(duration_row["service_duration_min"])
        
        if not duration_row:
            conn.close()
            flash("Selected service not found", "danger")
            return redirect(url_for('Book'))
        

        hh, mm = map(int, time.split(':'))
        total_min = hh*60 + mm
        if total_min < 8*60 or total_min > 17*60:
            conn.close()
            flash("Unavailable during non-business hours", "danger")
            return redirect(url_for('Book'))
        
        if total_min + duration_min > 17*60:
            conn.close()
            flash("Service not available during non-business hours", "danger")
            return redirect(url_for('Book'))
        
        if not is_slot_available(conn, stylist_id, start_dt, duration_min):
            conn.close()
            flash("Stylist already booked in that time slot", "danger")
            return redirect(url_for('Book', stylist_id=stylist_id))


        new_id = conn.execute(
            "INSERT INTO bookings (customer_email, service_id, stylist_id, start_datetime, duration_min) VALUES (?, ?, ?, ?, ?)",
            (customer_email, service_id, stylist_id, start_dt, duration_min)
        ).lastrowid
        conn.commit()
        conn.close()
        flash("Booking created", "success")
        return redirect(url_for('Book', stylist_id=stylist_id))
    
    selected_service = request.args.get('service_id')
    selected_date = request.args.get('date')
    selected_stylist = request.args.get('stylist_id')

    slots = []
    if selected_service and selected_date and selected_stylist:
        row = conn.execute("SELECT service_duration_min FROM services WHERE service_id = ?", (selected_service,)).fetchone()
        if row:
            duration_min = int(row["service_duration_min"])
            candidate_slots = generate_slots_for_date(duration_min, selected_date)
            slots = []
            for t in candidate_slots:
                start_dt = f"{selected_date} {t}:00"
                if is_slot_available(conn, selected_stylist, start_dt, duration_min):
                    slots.append(t)
    conn.close()
    return render_template("Book.html", 
                           services=services, 
                           stylists=stylists,
                           slots=slots, 
                           selected_service=selected_service,
                           selected_date=selected_date, 
                           selected_stylist=selected_stylist)

@app.route("/login")
def login():
    return render_template("login.html")  


@app.route("/AboutUs")
def AboutUs():
    conn = get_db_connection()
    hairdressor = conn.execute('SELECT * FROM hairdressor').fetchall()
    conn.close()
    return render_template("AboutUs.html", hairdressor=hairdressor)  

@app.route('/products', methods=['GET', 'POST'])
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
        'WomanTrim': "Womans Trim.jpg",
        'WomanCut': "Womans Cut.jpg",
        'MenCut': "Mens cut.webp",
        'Balayage': 'Balayage.jpg',
        'Highlights': 'Highlights.jpg',
        'Semi-permanent colour': 'Semi-permanent colour.webp',
        'Toner': 'Toner.webp',
        'Lowlights': 'Lowlights.jpg',
        'Permanent colour': 'permanent colour.jpg'
    }
    
    return render_template('services.html', services=services, service_images=service_images)


@app.route("/customer_login", methods=['GET', 'POST'])
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
            session['customer_id'] = customer['customer_id']
            session['customer_name'] = customer['customer_name']
            session['customer_surname'] = customer['customer_surname']
            
            image_name = customer['customer_name'].lower() + ".jpeg"
            session['customer_image'] = image_name
            
            return redirect(url_for('customer_homepage'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('customer_login'))
    return render_template("customer_login.html")  

@app.route("/customer_homepage")
def customer_homepage():
    if 'customer_id' not in session:
        return redirect(url_for('customer_login'))

    return render_template(
    "customer_homepage.html",
    name=session['customer_name'],
    surname=session['customer_surname'],
    image=session['customer_image']
)


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

@app.route("/My_Schedule", methods=['GET', 'POST'])
def My_Schedule():
    stylist_id = request.args.get('stylist_id') 
    import datetime
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        conn = get_db_connection()
        conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('My_Schedule', stylist_id=stylist_id))
    
    conn = get_db_connection()


    stylists = conn.execute(
        "SELECT hairdressor_id AS id, hairdressor_name || ' ' || hairdressor_surname AS name FROM hairdressor"
    ).fetchall()
     
    q = """
      SELECT b.id, b.start_datetime, b.duration_min, b.end_datetime,
             s.service_name, h.hairdressor_name || ' ' || h.hairdressor_surname AS stylist_name,
             b.customer_email, b.stylist_id
      FROM bookings b
      LEFT JOIN services s ON b.service_id = s.service_id
      LEFT JOIN hairdressor h ON b.stylist_id = h.hairdressor_id
    """
    params = []
    if stylist_id:
        q += " WHERE b.stylist_id = ?"
        params.append(stylist_id)
    q += " ORDER BY b.start_datetime"

    rows = conn.execute(q, params).fetchall()


    bookings = []
    import datetime
    for r in rows:
        try:
            dt = datetime.datetime.strptime(r['start_datetime'], "%Y-%m-%d %H:%M:%S")
        except Exception:
            dt = datetime.datetime.strptime(r['start_datetime'][:16], "%Y-%m-%d %H:%M")
        bookings.append({
            "id": r["id"],
            "day": dt.weekday(),
            "time": dt.strftime("%H:%M"),
            "client": r["customer_email"] or '',
            "service": r["service_name"] or '',
            "stylist": r["stylist_name"] or '',
            "stylist_id": r["stylist_id"]
        })

    conn.close()

    
    return render_template("My_Schedule.html",
                            bookings=bookings, 
                            stylists=stylists, 
                            selected_stylist=stylist_id)

@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html") 

@app.route('/update_product', methods=['POST'])
def update_product():
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    product_category = request.form.get('product_category')
    stock_quantity = request.form.get('stock_quantity')
    price = request.form.get('price')

    conn = get_db_connection()
    conn.execute(
        'UPDATE PRODUCTS SET product_name=?, product_category=?, stock_quantity=?, price=? WHERE product_id=?',
        (product_name, product_category, int(stock_quantity), float(price), product_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('Inventory_levels')) 

@app.route('/Customer_Schedule')
def Customer_Schedule():
    return render_template("Customer_Schedule.html")

if __name__ == "__main__":
    app.run(debug=True)





