from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from database import get_connection, create_tables

app = Flask(__name__)

create_tables()

@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flavors")
    flavors = cursor.fetchall()
    conn.close()
    return render_template('index.html', flavors=flavors)

@app.route('/add_to_cart/<int:flavor_id>')
def add_to_cart(flavor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (flavor_id) VALUES (?)", (flavor_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT flavors.name 
                      FROM cart 
                      JOIN flavors ON cart.flavor_id = flavors.id''')
    cart_items = cursor.fetchall()
    conn.close()
    return render_template('cart.html', cart_items=cart_items)


@app.route('/add_allergen', methods=['POST'])
def add_allergen():
    allergen_name = request.form.get('allergen')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO allergens (name) VALUES (?)", (allergen_name,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/search')
def search():
    query = request.args.get('query')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flavors WHERE name LIKE ?", (f'%{query}%',))
    results = cursor.fetchall()
    conn.close()
    return render_template('flavors.html', flavors=results)

@app.route('/allergens')
def view_allergens():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM allergens")
    allergens = cursor.fetchall()
    conn.close()
    return render_template('allergens.html', allergens=allergens)

@app.route('/suggest_flavor', methods=['POST'])
def suggest_flavor():
    suggestion = request.form.get('flavor')
    if suggestion:  
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO flavor_suggestions (suggestion) VALUES (?)", (suggestion,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/view_suggestions')
def view_suggestions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT suggestion FROM flavor_suggestions")
    suggestions = cursor.fetchall()
    conn.close()
    return render_template('suggestions.html', suggestions=suggestions)




if __name__ == '__main__':
    app.run(debug=True)
