from flask import request, jsonify
from . import bp
from app.models import User

# verify a user
@bp.post('/verifyuser')
def verify_user():
    content = request.json
    thisUsername = content['username'] # written like this assuming we're keying into a passed in json obj
    thisPassword = content['password']
    thisUser = User.query.filter_by(username=thisUsername).first()
    if thisUser and thisUser.check_password(thisPassword):
        return jsonify([{'user token': thisUser.token}])
    return jsonify({'message':'Invalid user info'})

# register a user
@bp.post('/registeruser')
def register_user():
    content = request.json
    thisUsername = content['username'] # written like this assuming we're keying into a passed in json obj
    thisEmail = content['email'] # again, this is all predicated on user posting a json file here.
    thisPassword = content['password']
    thisUserCheck = User.query.filter_by(username=thisUsername).first()
    if thisUserCheck:
        return jsonify([{'message':'Username taken, try again.'}])
    thisEmailCheck = User.query.filter_by(email=thisEmail).first()
    if thisEmailCheck:
        return jsonify([{'message':'Username taken, try again.'}])
    thisNewUser = User(email = thisEmail, username=thisUsername)
    thisNewUser.password = thisNewUser.hash_password(thisPassword)
    thisNewUser.add_token()
    thisNewUser.commit()
    print(thisNewUser)
    return jsonify([{'message': f"{thisNewUser.username} registered"}])
    
