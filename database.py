from app import *

# Create new post
def create_post(title, content):
    conn = connect_db()
    c = conn.cursor()

    # Insert post into database
    c.execute("INSERT INTO posts(title, content) VALUES (?, ?)" ,(title, content))

    conn.commit()
    conn.close()


def check_login(username, password):
    conn = connect_db()
    print("checking login")
    if (conn is None):
        return None
    c = conn.cursor()

    try:
        sql = c.execute("""SELECT * FROM users WHERE username=%s""", username, password)
        c.close()
        conn.close()
        return sql
    except:
        print("Error Invalid Login")
    c.close()
    conn.close()
    return None