from flask import Flask
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask import jsonify
from flask import request
from flask_restful import Resource,Api
from flask_httpauth import HTTPBasicAuth

webservice=Flask(__name__)
webservice.config['SECRET']="secret!123"
socketio=SocketIO(webservice, cors_allowed_origins="*")

api=Api(webservice,prefix="/api/v1")
auth=HTTPBasicAuth()
auth1=HTTPBasicAuth()

admin_data={
    "admin":"admin_password",
}
adminanduser_data={
    "admin":"admin_password",
    "normal_user": "user_password"
}

UsersDB=[{
    'name':'Rahul',
    'Phoneno':'837393993'
},
    {'name':'Ganesh',
     'Phoneno':'948947590'
}]

@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    if message !="User connected!":
        send(message, broadcast=True)

@webservice.route('/')
def index():
    return render_template("index.html")

@auth.verify_password
def verify(username,password):

    return admin_data.get(username)==password

@auth1.verify_password
def verify(username,password):

    return adminanduser_data.get(username)==password

@webservice.route("/users",methods=['GET'])
@auth1.login_required
def get_allusers():
    return jsonify({"users":UsersDB})

@webservice.route("/users/<name>",methods=['GET'])
@auth1.login_required
def search_user(name):
    user_details=[user for user in UsersDB if(name.lower() in user['name'].lower())]
    print(user_details)
    return jsonify({"users":user_details})

@webservice.route("/users/createuser",methods=['POST'])
@auth.login_required #only admin can create user
def create_user():
    user={
        'name': request.json['name'],
        'Phoneno':request.json['Phoneno']
    }
    UsersDB.append(user)
    return jsonify({"users":UsersDB})

@webservice.route("/users/edituser/<Phoneno>",methods=['PUT'])
@auth.login_required  # only admin can edit user
def edit_user(Phoneno):
    user_value=[user for user in UsersDB if (user['Phoneno']==Phoneno)]
    if(user_value[0]['Phoneno']== request.json['Phoneno']):
        print("User is available")
    if('name' in request.json):
        user_value[0]['name']=request.json['name']
    return jsonify({"users":user_value[0]})

@webservice.route("/users/deleteuser/<Phoneno>",methods=['DELETE'])
@auth1.login_required
def delete_user(Phoneno):
    user_value=[user for user in UsersDB if(user['Phoneno']==Phoneno)]
    UsersDB.remove(user_value[0])
    return jsonify({"users":UsersDB})

if (__name__=="__main__"):
    socketio.run(webservice,host="localhost",allow_unsafe_werkzeug=True)
    #webservice.run()