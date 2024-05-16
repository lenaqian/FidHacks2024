from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

# Dummy user data (replace this with your user authentication mechanism)
users = {
    'user1': {'email': 'user1@example.com', 'password': 'password1', 'role': 'mentor', 'priority': 'Negotiation tactics'},
    'user2': {'email': 'user2@example.com', 'password': 'password2', 'role': 'mentee', 'priority': 'Investing'}
}

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = users[session['username']]
        return render_template('dashboard.html', username=session['username'], email=user['email'], role=user['role'], priority=user['priority'])
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/make_account', methods=['GET', 'POST'])
def make_account():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        role = request.form['role']
        email = request.form['email']
        priority = request.form['priority']

        # Process the data (store in database, etc.)
        # For now, just print the data
        print('Role:', role)
        print('Email:', email)
        print('Priority:', priority)

        # Redirect to a confirmation page
        return render_template('confirmation.html', role=role, email=email, priority=priority)
    else:
        return render_template('make_account.html', priority_items=priority_items)





