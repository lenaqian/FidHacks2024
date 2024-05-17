from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production


# Dummy user data (replace this with your user authentication mechanism)
users = {    'user1': {'email': 'user1@example.com', 'password': 'password1', 'role': 'mentor', 'priorities': ['Networking', 'Education']},
    'user2': {'email': 'user2@example.com', 'password': 'password2', 'role': 'mentee', 'priorities': ['Investment', 'Healthcare']}
}

# Dummy mentee data (replace this with your actual mentee data)
mentees = [
    {'name': 'Alice', 'email': 'alice@example.com', 'priorities': ['Networking', 'Education']},
    {'name': 'Bob', 'email': 'bob@example.com', 'priorities': ['Investment', 'Healthcare']}
]

priority_items = ["Investment", "Networking", "Retirement", "Healthcare", "Education"]

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'make_account/profile' in request.form:  # Check if the user clicked the "Create Account" button
            # Handle account creation logic here
            # You can render a different template for account creation or redirect to a separate route for account creation
            return redirect('/make_account/profile')  # Redirect to the account creation page
        else:
            # Handle login logic here
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
        if user['role'] == 'mentor':
            # mentor_priorities = user['priority'].split(',')
            mentor_priorities = user['priorities']

            matches = []
            for mentee in mentees:
                if any(priority in mentee['priorities'] for priority in mentor_priorities):
                    matches.append(mentee)
            return render_template('mentor_dashboard.html', matches=matches)
        else:
            return render_template('mentee_dashboard.html')
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
        
        # priority = request.form['priority']
        # selected_priorities = request.form.getlist('priority')
        # # Get form data
        username = session['username']
        # users[username]['priorities'] = selected_priorities

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




        # Process the data (store in database, etc.)
        # For now, just print the data
        # print('Role:', role)
        # print('Email:', email)
        # print('Priority:', priority)

        # Redirect to interests selection page
        return redirect('/make_account/interests')
        #return render_template('confirmation.html', email=email, role=role, selected_priorities=selected_priorities)
    
    else:
        return render_template('make_account_profile.html', priority_items=priority_items)
    

@app.route('/make_account/interests', methods=['GET', 'POST'])
def make_account_interests():
    if request.method == 'POST':
        # Get form data
        selected_priorities = request.form.getlist('priority')
        # selected_priorities_list = list(selected_priorities)

        # Process the data (store in database, etc.)
        # For now, just print the data
        # print('Role:', role)
        # print('Email:', email)
        # print('Priority:', priority)

        # Redirect to interests selection page
        # users[session['username']['priorities']] = selected_priorities
        username = session['username']
        users[username]['priorities'] = selected_priorities
        role = users[username]['role']
        name = users[username]['name']
        email = users[username]['email']
        
        # return render_template('confirmation.html', selected_priorities=selected_priorities)
        return render_template('confirmation.html', email=email, name=name, role=role, selected_priorities=selected_priorities)
    
    else:
        return render_template('make_account_interests.html', priority_items=priority_items)


if __name__ == '__main__':
    app.run(debug=True)



