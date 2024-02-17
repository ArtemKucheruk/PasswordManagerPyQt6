import sqlite3

def create_table():

    con = sqlite3.connect("passwords/db_for_passwords.db")
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS db_for_passwords (
            name_second TEXT,
            password_second TEXT,
            info_second TEXT
        );
    ''')

    con.commit()
    cur.close()
    con.close()
def register_second(name_second, password_second, info_second, mysignalsecond):

    try:
        with sqlite3.connect("passwords/db_for_passwords.db") as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM db_for_passwords WHERE name_second=?;', (password_second,))
            value = cur.fetchall()

            if value:
                mysignalsecond.emit('This nickname already exists')
            else:
                cur.execute("INSERT INTO db_for_passwords (name_second, password_second, info_second) VALUES (?, ?, ?);",
                            (name_second, password_second, info_second))
                mysignalsecond.emit('Success adding new password')
                con.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        cur.close()
        con.close()