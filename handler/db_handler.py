import sqlite3


def create_users_table():
    CREATE_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    );
    '''
    conn = sqlite3.connect('handler/users.db')  # Provide the full path to your database file
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_QUERY)
    conn.commit()
    conn.close()

def login(login, passw, signal):
    try:
        con = sqlite3.connect('handler/Users.db')  # Provide the full path to your database file
        cur = con.cursor()

        cur.execute('SELECT * FROM users WHERE name=? AND password=?;', (login, passw))
        value = cur.fetchall()

        if value:
            signal.emit("Login success")
        else:
            signal.emit("Check your password or login")

    except Exception as e:
        signal.emit(f"Error: {str(e)}")
    finally:
        con.close()

def reg(name, password, signal):
    try:
        con = sqlite3.connect('handler/users.db')  # Provide the full path to your database file
        cur = con.cursor()

        # Check if the username already exists
        cur.execute('SELECT * FROM users WHERE name=?;', (name,))
        if cur.fetchone() is not None:
            signal.emit("Username already exists. Please choose a different one.")
            return

        # Insert the new user
        cur.execute('INSERT INTO users (name, password) VALUES (?, ?);', (name, password))
        con.commit()
        signal.emit("Registration success")

    except Exception as e:
        signal.emit(f"Error: {str(e)}")
    finally:
        con.close()

# Call the create_users_table function to ensure the users table exists
create_users_table()