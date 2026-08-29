from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ecommerce_secret_key"


# ---------------- DATABASE ----------------

def get_db_connection():
    conn = sqlite3.connect("ecommerce.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_date TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- PRODUCTS ----------------

products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "price": 1499,
        "image": "images/headphones.jpg"
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "price": 2499,
        "image": "images/smartwatch.jpg"
    },
    {
        "id": 3,
        "name": "Bluetooth Speaker",
        "price": 999,
        "image": "images/speaker.jpg"
    },
    {
        "id": 4,
        "name": "USB Keyboard",
        "price": 799,
        "image": "images/keyboard.jpg"
    }
]


# ---------------- HOME PAGE ----------------

@app.route("/")
def index():
    return render_template("index.html", products=products)


# ---------------- ADD TO CART ----------------

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    session["cart"] = cart

    return redirect(url_for("cart"))


# ---------------- CART ----------------

@app.route("/cart")
def cart():

    cart = session.get("cart", {})

    cart_items = []
    total = 0

    for product in products:

        product_id = str(product["id"])

        if product_id in cart:

            quantity = cart[product_id]

            subtotal = product["price"] * quantity

            cart_items.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal
            })

            total += subtotal

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


# ---------------- UPDATE CART ----------------

@app.route("/update_cart/<int:product_id>/<action>")
def update_cart(product_id, action):

    cart = session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:

        if action == "increase":
            cart[product_id] += 1

        elif action == "decrease":
            cart[product_id] -= 1

            if cart[product_id] <= 0:
                del cart[product_id]

    session["cart"] = cart

    return redirect(url_for("cart"))


# ---------------- REMOVE FROM CART ----------------

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    session["cart"] = cart

    return redirect(url_for("cart"))


# ---------------- CHECKOUT PAGE ----------------

@app.route("/checkout")
def checkout():

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("index"))

    cart_items = []
    total = 0

    for product in products:

        product_id = str(product["id"])

        if product_id in cart:

            quantity = cart[product_id]
            subtotal = product["price"] * quantity

            cart_items.append({
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": subtotal
            })

            total += subtotal

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total
    )


# ---------------- PLACE ORDER ----------------

@app.route("/place_order", methods=["POST"])
def place_order():

    customer_name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("index"))

    total = 0

    for product in products:

        product_id = str(product["id"])

        if product_id in cart:
            total += product["price"] * cart[product_id]

    # Save order
    conn = get_db_connection()

    cursor = conn.execute("""
        INSERT INTO orders
        (customer_name, email, phone, address, total_amount, order_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        customer_name,
        email,
        phone,
        address,
        total,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    order_id = cursor.lastrowid

    # Save order items
    for product in products:

        product_id = str(product["id"])

        if product_id in cart:

            quantity = cart[product_id]

            conn.execute("""
                INSERT INTO order_items
                (order_id, product_name, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (
                order_id,
                product["name"],
                quantity,
                product["price"]
            ))

    conn.commit()
    conn.close()

    # Clear cart
    session["cart"] = {}

    return render_template(
        "success.html",
        order_id=order_id,
        customer_name=customer_name,
        total=total
    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)