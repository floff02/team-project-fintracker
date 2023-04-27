from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector, json

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.secret_key = 'your_secret_key'

# Connect to the database
cnx = mysql.connector.connect(host='localhost',
                              user='root',
                              password='X#n!WNnZKIPh7LCk',
                              database='fintracker')



# Setup routing
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def homerender():
    return render_template('home.html')

@app.route('/fintracker')
def fintrackerrender():
    try:
        messages = session['messages']
        return render_template('fintracker.html', messages=json.loads(messages))
    except:
        return redirect('/')

@app.route('/login')
def loginrender():
    return render_template('login.html')

@app.route('/about')
def aboutrender():
    return render_template('about.html')

@app.route('/subs')
def subsrender():
    return render_template('subs.html')

@app.route('/signup')
def signuprender():
    return render_template('signup.html')

# Setup processing
@app.route('/login', methods=['POST'])
def login():
    # Get the user's input from the form
    email = request.form['email']
    password = request.form['password']
    
    # Create a cursor
    cursor = cnx.cursor()

    # Check if the user exists in the database
    query = 'SELECT * FROM users WHERE email = %s AND password = %s'
    cursor.execute(query, (email, password))

    # Fetch the results
    results = cursor.fetchall()

    # If the user exists, log them in
    if results:
        current_user = results[0][0]
        session["messages"] = json.dumps({"username":current_user})
        return redirect("/fintracker")
    # If the user doesn't exist, redirect to the signup page
    else:
        return redirect('/signup')

@app.route('/signup', methods=['POST'])
def signup():
    # Get the user's input from the form
    fname = request.form['fname']
    sname = request.form['sname']
    email = request.form['email']
    password = request.form['password']
    cursor = cnx.cursor()
    query = 'INSERT INTO users (fname, sname, email, password) VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (fname, sname, email, password))
    cnx.commit()
    cursor.close()
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('messages')
    return redirect('/about')

if __name__ == '__main__':
    app.run(debug=True)