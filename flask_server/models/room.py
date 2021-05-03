from server import db
from datetime import datetime

def get(code):
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT * FROM rooms WHERE code=%s", (code, ))
        records = cursor.fetchall()
        db.conn.commit()
        cursor.close()
        if len(records) != 0:
            record = records[0]
            roomcode = record[0]
            creator = record[1]
            return {'code': roomcode, 'createdby': creator}   
        return None
    except Exception as e:
        print(e)
        return None
    
def getUsers(code):
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT * FROM users u WHERE u.username IN (SELECT j.username FROM joins j WHERE roomcode=%s)", (code, ))
        records = cursor.fetchall()
        db.conn.commit()
        cursor.close()
        if len(records) != 0:
            return [{"username": record[0], "name": record[2]} for record in records]  
        return []
    except Exception as e:
        print(e)
        return None

def create(data):
    code = data["code"]
    creator = data["username"]
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "INSERT INTO rooms (code, createdby) VALUES(%s, %s)", (code, creator))
        db.conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def join(data):
    roomcode = data["code"]
    username = data["username"]
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "INSERT INTO joins (username, roomcode) VALUES(%s, %s)", (username, roomcode))
        db.conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def insertMessage(data):
    roomcode = data["code"]
    sender = data["username"]
    content = data["content"]
    now = str(datetime.now())
    
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "INSERT INTO messages (content, datetime, sender, roomcode) VALUES(%s, %s, %s, %s) RETURNING id", (content, now, sender, roomcode))
        db.conn.commit()
        inserted_id = cursor.fetchone()[0]
        cursor.close()
        return {'content': content, 'sender': sender, 'datetime': now, 'id': inserted_id}
    except Exception as e:
        print("insertMessage:" + e)
        return False
    
def fetchMessages(code):
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT * FROM messages WHERE roomcode=%s", (code, ))
        records = cursor.fetchall()
        db.conn.commit()
        cursor.close()
        if len(records) != 0:
            return [{"content": record[1], "datetime": record[2], "sender": record[3]} for record in records] 
        return []
    except Exception as e:
        print(e)
        return None
    
