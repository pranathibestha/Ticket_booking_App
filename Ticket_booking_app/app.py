from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize or create the database
def init_db():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            event TEXT,
            tickets INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Booking page
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        event = request.form['event']
        tickets = request.form['tickets']

        conn = sqlite3.connect('tickets.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, event, tickets) VALUES (?, ?, ?)", (name, event, tickets))
        conn.commit()
        conn.close()
        return render_template('confirmation.html', name=name, event=event, tickets=tickets)
    return render_template('booking.html')

# View all bookings
@app.route('/view')
def view_bookings():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return render_template('view_bookings.html', bookings=bookings)

# Reset/Delete all bookings
@app.route('/reset')
def reset_table():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS bookings")
    c.execute('''
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            event TEXT,
            tickets INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    return "🧹 All bookings have been deleted and table reset successfully!"

if __name__ == '__main__':
    app.run(debug=True)
