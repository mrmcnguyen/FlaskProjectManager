from app import *

# Check user login
def check_login(username, password):
    conn = connect_db()
    print("checking login")
    if (conn is None):
        return None
    c = conn.cursor()

    try:
        sql = c.execute("""SELECT * FROM users WHERE username=? AND password=?""", (username, password))
        results = sql.fetchall()
        print(results)
        c.close()
        conn.close()
        return results
    except:
        print("Error Invalid Login")
    c.close()
    conn.close()
    return None