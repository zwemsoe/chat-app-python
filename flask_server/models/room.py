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
            "SELECT username FROM users u WHERE u.username IN (SELECT j.username FROM joins j WHERE roomcode=%s)", (code, ))
        records = cursor.fetchall()
        db.conn.commit()
        cursor.close()
        if len(records) != 0:
            return [record[0] for record in records]  
        return []
    except Exception as e:
        print(e)
        return None

def userInRoom(data):
    code = data["code"]
    username = data["username"]
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT username FROM joins WHERE roomcode=%s AND username=%s ", (code, username))
        records = cursor.fetchall()
        db.conn.commit()
        cursor.close()
        if len(records) != 0:
            return True
        return False
    except Exception as e:
        print(e)
        return None

def getRooms(username):
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT * FROM rooms WHERE code IN (SELECT roomcode FROM joins WHERE username=%s)", (username, ))
        records = cursor.fetchall()
        db.conn.commit()
        cursor.close()
        if len(records) != 0:
            return [{"roomcode": record[0], "createdby": record[1]} for record in records]  
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
        print(e)
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
    
def leave(data):
    roomcode = data["roomcode"]
    username = data["username"]
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "DELETE FROM joins WHERE roomcode=%s AND username=%s", (roomcode, username))
        db.conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def delete(data):
    roomcode = data["roomcode"]
    username = data["username"]
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "DELETE FROM rooms WHERE code=%s AND createdby=%s", (roomcode, username))
        cursor.execute(
            "DELETE FROM joins WHERE roomcode=%s", (roomcode,))
        db.conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False

def deleteMessages(roomcode):
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            "DELETE FROM messages WHERE roomcode=%s", (roomcode,))
        db.conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False