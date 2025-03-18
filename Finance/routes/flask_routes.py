from flask import Blueprint, render_template, request, redirect
from database.db import Database

flask_bp = Blueprint('flask', __name__)
db = Database()

@flask_bp.route('/')
def index():
    cursor = db.get_connection().cursor(dictionary=True)
    cursor.execute("SELECT * FROM chits")
    chits = cursor.fetchall()
    cursor.close()
    return render_template('index.html', chits=chits)

@flask_bp.route('/add', methods=['POST'])
def add_chit():
    try:
        chit_name = request.form['chit_name']
        amount = float(request.form['amount'])
        duration = int(request.form['duration'])
        members = int(request.form['members'])
        
        cursor = db.get_connection().cursor()
        cursor.execute(
            "INSERT INTO chits (chit_name, amount, duration_months, total_members) VALUES (%s, %s, %s, %s)",
            (chit_name, amount, duration, members)
        )
        db.get_connection().commit()
        cursor.close()
        return redirect('/')
    except Exception as e:
        print(f"Error adding chit: {e}")
        return redirect('/')  # Optionally, redirect to an error page
