import requests
from functools import wraps

class TokenNotAuthenticated(Exception):
    pass

Token = None
login_url = 'http://127.0.0.1:5000/login'
register_url ='http://127.0.0.1:5000/register'

def token_required(f):
    @wraps(f)
    def innerfun(*arg,**kwargs):
        if Token != None:
            return f(*arg,**kwargs)
        else:
            print("user not authenticated")
    return innerfun



def authenticate(username,password):
    global Token
    res = requests.get(login_url,auth=(username,password))
    if res.headers.get('x-auth-token'):
        Token =  res.headers['x-auth-token']
        return res.status_code
    return res.status_code


def register(username,password):
    res =  requests.get(register_url,json={"username":username,"password":password})
    return res.status_code

@token_required
def get_resource(uri=None):
    res = requests.get(uri,headers={"x-auth-token":Token}) 
    return res.json()

@token_required
def post_resource():
    pass

@token_required
def delete_resource():
    pass

@token_required
def put_resource():
    pass

