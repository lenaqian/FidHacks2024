from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = 'fid'  # Change this to a secure secret key in production

# Dummy user data
users = {    'user1': {'email': 'user1@example.com', 'password': 'password1', 'role': 'mentor', 'priorities': ['Beginning Investing', 'Work-Life Balance']},
    'user2': {'email': 'user2@example.com', 'password': 'password2', 'role': 'mentee', 'priorities': ['Intro to Stocks', 'Finding Job Opportunities']}
}

# Dummy mentee data 
mentees = [
    {'name': 'Alice', 'email': 'alice@example.com', 'priorities': ['Beginning Investing', 'Work-Life Balance']},
    {'name': 'Bob', 'email': 'bob@example.com', 'priorities': ['Intro to Stocks', 'Finding Job Opportunities']},
    {'name': 'Nivedita', 'email': 'nive@example.com', 'priorities': ['Intro to Stocks', 'Intro to Crypto', 'Finding Job Opportunities']},
    {'name': 'David', 'email': 'david@example.com', 'priorities': ['Transitioning to a New Job', 'Work-Life Balance']},
    {'name': 'Eve', 'email': 'eve@example.com', 'priorities': ['Intro to Crypto', 'Retirement Plans']},
    {'name': 'Frank', 'email': 'frank@example.com', 'priorities': ['Beginning Investing', 'Salary Negotiation']},
    {'name': 'Grace', 'email': 'grace@example.com', 'priorities': ['Finding Job Opportunities', 'Transitioning to a New Job']},
    {'name': 'Harry', 'email': 'harry@example.com', 'priorities': ['Work-Life Balance', 'Financial Basics']},
    {'name': 'Ivy', 'email': 'ivy@example.com', 'priorities': ['Intro to Stocks', 'Intro to Crypto']},
    {'name': 'Jack', 'email': 'jack@example.com', 'priorities': ['Salary Negotiation', 'Retirement Plans']}
]
# Dummy mentee data 
mentors = [
    {'name': 'Alice', 'email': 'alice@example.com', 'priorities': ['Beginning Investing', 'Work-Life Balance']},
    {'name': 'Bob', 'email': 'bob@example.com', 'priorities': ['Intro to Stocks', 'Finding Job Opportunities']},
    {'name': 'Nivedita', 'email': 'nive@example.com', 'priorities': ['Intro to Stocks', 'Intro to Crypto', 'Finding Job Opportunities']},
    {'name': 'David', 'email': 'david@example.com', 'priorities': ['Transitioning to a New Job', 'Work-Life Balance']},
    {'name': 'Eve', 'email': 'eve@example.com', 'priorities': ['Intro to Crypto', 'Retirement Plans']},
    {'name': 'Frank', 'email': 'frank@example.com', 'priorities': ['Beginning Investing', 'Salary Negotiation']},
    {'name': 'Grace', 'email': 'grace@example.com', 'priorities': ['Finding Job Opportunities', 'Transitioning to a New Job']},
    {'name': 'Harry', 'email': 'harry@example.com', 'priorities': ['Work-Life Balance', 'Financial Basics']},
    {'name': 'Ivy', 'email': 'ivy@example.com', 'priorities': ['Intro to Stocks', 'Intro to Crypto']},
    {'name': 'Jack', 'email': 'jack@example.com', 'priorities': ['Salary Negotiation', 'Retirement Plans']}
]

priority_items = ["Financial Basics", "Beginning Investing", "Intro to Stocks", "Intro to Crypto",
                   "Salary Negotiation", "Transitioning to a New Job", "Work-Life Balance", "Finding Job Opportunities", "Retirement Plans"]

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'make_account/profile' in request.form:  # Check if the user clicked the "Create Account" button
            # Handle account creation logic here
            return redirect('/make_account/profile')  # Redirect to the account creation page
        else:
            username = request.form['username']
            password = request.form['password']
            if username in users and users[username]['password'] == password:
                session['username'] = username
                return redirect('/dashboard')
            else:
                return render_template('login2.html', error='Invalid username or password')
    return render_template('login2.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = users[session['username']]
        if user['role'] == 'mentor':
            mentor_priorities = user['priorities']
            matches = []
            for mentee in mentees:
                if any(priority in mentee['priorities'] for priority in mentor_priorities):
                    matches.append(mentee)
            return render_template('mentor_dashboard.html', matches=matches)
        else:
            mentee_priorities = user['priorities']
            matches = []
            for mentor in mentors:
                if any(priority in mentor['priorities'] for priority in mentee_priorities):
                    matches.append(mentor)
            return render_template('mentee_dashboard.html', matches=matches)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')


@app.route('/make_account/profile', methods=['GET', 'POST'])
def make_account_profile():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        role = request.form['role']
        email = request.form['email']
        session['username'] = username

        # Create a new user dictionary
        new_user = {
            'email': email,
            'name' : name,
            'password': password,
            'role': role,
            'priorities': []
        }

        # Add the new user to the users dictionary
        users[username] = new_user

        # Redirect to interests selection page
        return redirect('/make_account/interests')
    
    else:
        return render_template('make_account_profile.html', priority_items=priority_items)
    

@app.route('/make_account/interests', methods=['GET', 'POST'])
def make_account_interests():
    if request.method == 'POST':
        # Get form data
        selected_priorities = request.form.getlist('priority')
        username = session['username']
        users[username]['priorities'] = selected_priorities
        role = users[username]['role']
        name = users[username]['name']
        email = users[username]['email']
        
        return render_template('confirmation.html', email=email, name=name, role=role, selected_priorities=selected_priorities)
    
    else:
        return render_template('make_account_interests.html', priority_items=priority_items)


if __name__ == '__main__':
    app.run(debug=True)



