from server import db, bcrypt

def save(data):
    name = data["name"]
    username = data["username"]
    password = data["password"]
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, name) VALUES(%s, %s, %s)", (username, hashed, name))
        db.conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False
        
        

def signin(data):
    username = data["username"]
    password = data["password"]
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=%s", (username,))
        records = cursor.fetchall()
        db.conn.commit()
        cursor.close()
        
        if len(records) != 0:
            record = records[0]
            db_password = record[1]
            matched = bcrypt.check_password_hash(db_password, password)
            if matched:
                return {"username": record[0], "name": record[2]}        
        return False
    except Exception as e:
        print(e)
        return False
