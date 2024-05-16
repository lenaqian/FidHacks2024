from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "fid"  # Used for session management, replace with your secret key

@app.route('/')
def home():
    return redirect('/login')

@app.route('/make_account', methods=['GET', 'POST'])
def make_account():
    if request.method == 'POST':
        # Get form data
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



@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        return render_template('dashboard.html')
    else:
        return redirect('/login')


