from flask import Flask, render_template_string, request, redirect, url_for
import pymssql  # Add this import for SQL connection

app = Flask(__name__)

# SQL Database connection settings
DB_SERVER = "bcghoutdn-server.database.windows.net"  # Example: myserver.database.windows.net
DB_DATABASE = "bcghoutdn-database"
DB_USERNAME = "bcghoutdn-server-admin"
DB_PASSWORD = "HVilA$7mzRVR$Ujg"

# HTML content for the login page
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
    
    if username and password:
        # Save username and password into SQL database
        try:
            conn = pymssql.connect(
                server=DB_SERVER,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                database=DB_DATABASE
            )
            cursor = conn.cursor()

            # You can create table if not exists (optional first time)
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
            CREATE TABLE users (
                id INT PRIMARY KEY IDENTITY(1,1),
                username NVARCHAR(255),
                password NVARCHAR(255)
            )
            """)

            # Insert the username and password
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, password))
            conn.commit()

            cursor.close()
            conn.close()
        except Exception as e:
            return f"Database error: {str(e)}"
        
        return redirect(url_for('hello', username=username))
    
    return redirect(url_for('home'))

# Route to display the greeting message
@app.route('/hello/<username>')
def hello(username):
    return f'Hello, {username}!'

if __name__ == '__main__':
    app.run(debug=True)
