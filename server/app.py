from flask import Flask,request,jsonify,make_response
import jwt
import base64
import datetime
from passlib.hash import pbkdf2_sha256
from database import DB , NoUserFound ,UniqueUserConstrain


SECRET_KEY = b'\xc0p8\xf7\x17\xf9\x874k\\r\xbd\x8a\xb8\x85/\xa6m\xd4\xf8)\xdf\x9b>'

def get_token(username):
    payload = {
        'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
        'usr':username
    }
    return jwt.encode(payload,SECRET_KEY,algorithm='HS256')

def decode_token(auth_token):
    print(auth_token)

    payload = jwt.decode(auth_token,SECRET_KEY,algorithm='HS256')
    username =  payload.get("usr")
    print("=========================================\n",username)
    return username




resourcelist =  {
    "uri":"/api/resource/",
    "Token_required":True
}


app = Flask(__name__)

@app.route('/login/',methods=['GET'])
def login():
    try:
        string =  request.headers['Authorization'].split()[1]
        string = base64.b64decode(string).decode('utf-8')
        username ,password = string.split(':')
        print(username,password)
        # We can easily get the username and pass from Authorization field by :- 'request.authorization'
        saved_pass = DB('userdb.db').getPass(username)
        if pbkdf2_sha256.verify(password,saved_pass):
            token = get_token(username)
            response = make_response('user verified',200)
            response.headers['x-auth-token'] = token
            return response
        else:
            return ('Unauthorized client',401)
    except NoUserFound:
        return ('No user found',404)
    
  
    
@app.route('/register/',methods=['GET'])
def register():
    try:
        data = request.get_json()
        print(request.headers)
        print(data)
        password = pbkdf2_sha256.hash(data.get('password')) 
        dbobj = DB('userdb.db')
        dbobj.createUser(data.get('username'),password)
        return ("registration successful",200)
    except UniqueUserConstrain:
        return ('Duplicate entry',409)


@app.route("/api/resource/")
def resource():
    try:
        if request.headers.get("x-auth-token"):
            auth_token = request.headers.get("x-auth-token")
            database = DB("userdb.db")
            print('===========================================\n',auth_token)
            resource = database.get_resources(decode_token(auth_token))
            print("================================================\n",resource)
            response = make_response({"dates":resource,"uri":"/api/resource/<string:month>"})
            return response
        else:
            raise jwt.exceptions.ExpiredSignatureError

    except jwt.exceptions.ExpiredSignatureError:
        return ('Token expired',400)

@app.route("/api/resource/<string:month>")
def get_month(username,month):
    pass

@app.route("/api/create_resource/",methods=["GET","POST"])
def create_resource():
    if request.method == "POST":
        database = DB("userdb.db")
        data = request.get_json()
        database.create_recource(data.get("username"),data.get("date"),data.get("expenditure"))
        return "success"

@app.errorhandler(404)
def not_found(error):
    return ('url not found',404)


if __name__ == "__main__":
    app.run(debug=True)

    
