from flask import request, jsonify
from flask_socketio import join_room, emit, leave_room
from models import room

online = {}

# Helpers 
def addOnlineUsers(roomcode, username):
    if roomcode in online:
        if username not in online[roomcode]:
            online[roomcode].append(username)
    else:
        online[roomcode] = []
        online[roomcode].append(username)

def sendUsers(roomcode, username):     
    addOnlineUsers(roomcode, username)   
    users = room.getUsers(roomcode)
    not_online = list(set(users) - set(online[roomcode]))
    emit('room users', {'online': online[roomcode], 'not_online': not_online}, to=roomcode, include_self=True)


# Socket Event-Handlers
def joinRoom(data):
    roomcode = data["code"]
    username = data["username"]
    print(username + " joined "+ roomcode)
    data = {'code': roomcode, 'username': username}
    
    result = room.userInRoom(data)
    if not result:
        exists = room.get(roomcode)
        if exists == None:
            room.create(data)
        room.join(data)
    join_room(roomcode)
    
    sendUsers(roomcode, username)

def sendMessage(data):
    roomcode = data["code"]
    username = data["username"]
    content = data["message"]
    
    print(username + " sent "+ content + " to " + roomcode)
    
    data = {'code': roomcode, 'username': username, 'content': content}
    sent_msg = room.insertMessage(data)
    
    if sent_msg:
        emit('new message', sent_msg , to=roomcode, include_self=True)
        


# REST ENDPOINTS
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
    
def getJoinedRooms(username):
    rooms = room.getRooms(username)
    if rooms != None:
        return jsonify({
            "success": True,
            "rooms": rooms
        })
    return jsonify({
          "success": False  
    })
    
def leaveRoom():
    data = request.get_json()
    result = room.leave(data)
    return jsonify({
          "success": result
    })   
    
def deleteRoom():
    data = request.get_json()
    result1 = room.leave(data)
    result2 = room.delete(data)
    result3 = room.deleteMessages(data["roomcode"])
    return jsonify({
          "success": result1 and result2 and result3
    })   