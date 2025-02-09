from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Database model for user authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('budget'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/budget')
def budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('budget.html', sections=budget_sections)

@app.route('/actual-costs')
def actual_costs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('actual_costs.html', sections=budget_sections)

# Sample budget sections extracted from the Excel file
budget_sections = [
    {"category": "General Requirements", "items": [
        "Architectural Plans and Specs", "Plan Review", "Permits", "Survey", "Impact Fee", 
        "Administrative Costs", "Financing Costs", "Legal Fees", "Engineering Fees", 
        "Insurance", "Budgeting Costs", "Client Meetings", "Sub-trade Meetings"
    ]},
    {"category": "Site Preparation", "items": [
        "Demolition", "Excavation", "Grading", "Soil Testing"
    ]},
    {"category": "Foundation", "items": [
        "Concrete Slab", "Footings", "Waterproofing", "Reinforcement"
    ]}
]

# Minimal HTML templates
login_html = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

register_html = """
<!DOCTYPE html>
<html>
<head><title>Register</title></head>
<body>
    <h2>Register</h2>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Register</button>
    </form>
</body>
</html>
"""

budget_html = """
<!DOCTYPE html>
<html>
<head><title>Budget</title></head>
<body>
    <h2>Budget Calculator</h2>
    {% for section in sections %}
        <h3>{{ section.category }}</h3>
        <ul>
            {% for item in section.items %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
</body>
</html>
"""

actual_costs_html = """
<!DOCTYPE html>
<html>
<head><title>Actual Costs</title></head>
<body>
    <h2>Actual Costs</h2>
    {% for section in sections %}
        <h3>{{ section.category }}</h3>
        <ul>
            {% for item in section.items %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
</body>
</html>
"""

if __name__ == '__main__':
    db.create_all()
app.run(debug=True, host='0.0.0.0', port=8080)




Initial commit

