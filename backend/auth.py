from utils import get_redis_connector
from db import User
from flask import Blueprint, jsonify, request
from functools import wraps
from uuid import uuid4

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

auth_api = Blueprint("auth", __name__, url_prefix="/auth")
SALT = bcrypt.gensalt()
UNAUTH_MESSAGE = "Unauthorized", 403

r = get_redis_connector()

def get_user_from_db(username):
    return User.query.where(User.username == username).first()

def generate_password_hash(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), SALT).decode("utf-8")

def authenticate_user(username, received_password):
    if not username or not received_password:
        return False
    
    user = get_user_from_db(username)
    if not username or not bcrypt.checkpw(received_password, user.password.encode("utf-8")):
        return False
    
    return user

def generate_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    iat = datetime.now(timezone.utc)
    cid = str(uuid4())

    if expires_delta:
        expire = iat + expires_delta
    else:
        expire = iat + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire, 
        "cid": cid,
        "iat": iat
    })

    r.set(to_encode["sub"], cid)
    r.expire(to_encode["sub"], ACCESS_TOKEN_EXPIRE_MINUTES*60)

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        actual_cid = payload.get("cid")
        expected_cid = str(r.get(username))
        
        if username is None: 
            print("cid not valid")
            return None
        
        if actual_cid != expected_cid:
            print(f"cid did not match, login again. Received {actual_cid}, expected {expected_cid}")
            return None
        
    except jwt.InvalidTokenError:
        return None
    user = get_user_from_db(username)
    return user

def get_logged_in_user():
    auth_header = request.headers.get('Authorization')
    jwt_token = None
    if auth_header and auth_header.startswith('Bearer '):
        jwt_token = auth_header.split(' ')[1]

    if not jwt_token:
        return None
    
    return get_current_user(jwt_token)

def auth_protected(fun):
    @wraps(fun)
    def foo(*args, **kwargs):
        current_user = get_logged_in_user()

        if not current_user:
            return UNAUTH_MESSAGE
        print("Got a valid user " + current_user.username)
        return fun(*args, **kwargs)
    return foo

@auth_api.get("/check")
def check():
    return "auth is active", 200

@auth_api.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password").encode("utf-8")

    user = authenticate_user(username, password)

    if not user:
        return UNAUTH_MESSAGE
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return jsonify({"access_token": access_token, "token_type": "bearer"})

def revoke_token(username: str):
    r.set(username, str(uuid4()))
    r.expire(username, ACCESS_TOKEN_EXPIRE_MINUTES)

@auth_api.post("/revoke")
def revoke_jwt_token():
    u = request.args.get("u")

    if not u:
        return "Invalid request", 400
    
    revoke_token(u)
    return "revoked", 200

@auth_api.get("/whoami")
def whoami():
    user = get_logged_in_user()
    if not user:
        return UNAUTH_MESSAGE
    return user.username


