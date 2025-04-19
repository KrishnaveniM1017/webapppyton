from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# HTML content for the login page (instead of using a separate HTML file)
login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form action="{{ url_for('login') }}" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>
        
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

# Route to show the login page
@app.route('/')
def home():
    return render_template_string(login_html)

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # If both fields are filled, redirect to the greeting page
    if username and password:
        return redirect(url_for('hello', username=username))
    return redirect(url_for('home'))  # Redirect back to login if inputs are empty

# Route to display the greeting message
@app.route('/hello/<username>')
def hello(username):
    return f'Hello, {username}!'

if __name__ == '__main__':
    app.run(debug=True)
