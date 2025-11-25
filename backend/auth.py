from db import User
from flask import Blueprint, jsonify, request
from functools import wraps

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

auth_api = Blueprint("auth", __name__, url_prefix="/auth")
SALT = bcrypt.gensalt()

AUTH_ERROR_MESSAGE = "Unauthorized", 403

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
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
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
            return AUTH_ERROR_MESSAGE
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
        return AUTH_ERROR_MESSAGE
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return jsonify({"access_token": access_token, "token_type": "bearer"})


@auth_api.get("/whoami")
def whoami():
    user = get_logged_in_user()
    if not user:
        return AUTH_ERROR_MESSAGE
    return user.username



