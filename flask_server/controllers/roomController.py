from flask import request, jsonify
from flask_socketio import join_room, emit
from models import room


def joinRoom(data):
    roomcode = data["code"]
    username = data["username"]
    socketId = data["socketId"]
    print(username + " joined "+ roomcode)
    data = {'code': roomcode, 'username': username}
    exists = room.get(roomcode)
    created = True
    if exists == None:
        created = room.create(data)
    joined = room.join(data)
    join_room(roomcode)
    users = room.getUsers(roomcode)
    if created and joined:
        emit('room users', {'users': users}, to=roomcode, include_self=True)

def sendMessage(data):
    roomcode = data["code"]
    username = data["username"]
    socketId = data["socketId"]
    content = data["message"]
    
    print(username + " sent "+ content + " to " + roomcode)
    
    data = {'code': roomcode, 'username': username, 'content': content}
    sent_msg = room.insertMessage(data)
    
    if sent_msg:
        emit('new message', sent_msg , to=roomcode, include_self=True)
        
def fetchOldMessages(roomcode):
    messages = room.fetchMessages(roomcode)
    if messages != None:
        return jsonify({
            "success": True,
            "messages": messages  
        })
    return jsonify({
          "success": False  
    })
    
        
    