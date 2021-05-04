from flask import request, session, jsonify
from models import user

def login():
    data = request.get_json()
    result = user.signin(data)
    if not result:
        return jsonify({
            "success": result,
        })
    else:
        session["auth_user"] = result
        return jsonify({
            "success": True,
            "data": result
        })

def register():
    data = request.get_json()
    result = user.save(data)
    return jsonify({
        "success": result
    })
    
def authuser():
    if "auth_user" in session:
        auth_user = session["auth_user"]
        
        return jsonify({
            "data": auth_user
        })
    return jsonify({
        "data": None
    })


def logout():
    session.pop("auth_user", None)
    return jsonify({
        "success": True
    })