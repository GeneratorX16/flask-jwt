import dotenv
import os

from flask_cors import cross_origin
dotenv.load_dotenv()

from enum import StrEnum
import math
from utils import get_redis_connector
from db import User, db
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from functools import wraps
from uuid import uuid4

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY_1= os.environ.get('JWT_SECRET_KEY_1')
SECRET_KEY_2= os.environ.get('JWT_SECRET_KEY_2')
SECRET_KEY_3= os.environ.get('JWT_SECRET_KEY_3')

ACTIVE_KEY = SECRET_KEY_1
ACTIVE_KID = "1"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


auth_api = Blueprint("auth", __name__, url_prefix="/auth")


class AuthMessage(StrEnum):
    UNAUTH_MESSAGE = "Unauthorized"
    TOKEN_EXPIRED = "your auth token has expired"
    TOKEN_REVOKED = "auth token revoked"
    INVALID_TOKEN = "invalid auth token provided"
    INVALID_CREDENTIALS = "invalid credentials"


r = get_redis_connector()

def get_user_from_db(username):
    return User.query.where(User.username == username).first()

def generate_password_hash(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def authenticate_user(username, received_password):
    if not username or not received_password:
        return False
    
    user = get_user_from_db(username)
    if not user:
        bcrypt.checkpw(received_password.encode("utf-8"), "DUMMY".encode("utf-8"))
        return False
    
    if not bcrypt.checkpw(received_password.encode("utf-8"), user.password.encode("utf-8")):
        return False
    
    return user

def generate_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    iat = datetime.now(timezone.utc)
    jti = str(uuid4())

    if expires_delta:
        expire = iat + expires_delta
    else:
        expire = iat + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire, 
        "jti": jti,
        "iat": iat
    })

    encoded_jwt = jwt.encode(to_encode, ACTIVE_KEY, algorithm=ALGORITHM, headers={"kid": ACTIVE_KID})
    return encoded_jwt


def get_logged_in_user():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        raise ValueError(AuthMessage.UNAUTH_MESSAGE)
    
    if not auth_header.startswith("Bearer ") or len(auth_header.split(" ")) != 2:
        raise ValueError(AuthMessage.INVALID_TOKEN)

    jwt_token = auth_header.split(" ")[1]

    if not auth_header.startswith("Bearer") or not jwt_token:
        raise ValueError(AuthMessage.UNAUTH_MESSAGE)
        
    try: 
        payload = jwt.decode(jwt_token, ACTIVE_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        jti = payload.get("jti")
        jti_is_blacklisted = bool(r.get(jti))

        if username is None: 
           raise ValueError(AuthMessage.TOKEN_EXPIRED)
        
        if jti_is_blacklisted:
            raise ValueError(AuthMessage.TOKEN_REVOKED)
        
    except jwt.InvalidTokenError:
        raise ValueError(AuthMessage.INVALID_TOKEN)
    
    user = get_user_from_db(username)
    return user

def auth_protected(fun):
    @wraps(fun)
    def foo(*args, **kwargs):
        current_user = None
        try:
            current_user = get_logged_in_user()
        except ValueError as e:
            msg = str(e)
            if AuthMessage.INVALID_CREDENTIALS in msg or AuthMessage.INVALID_TOKEN in msg or AuthMessage.TOKEN_EXPIRED in msg or AuthMessage.TOKEN_REVOKED in msg or AuthMessage.UNAUTH_MESSAGE in msg:
                return msg, 403
            else:
                raise e
        
        return fun(current_user = current_user, *args, **kwargs)
    return foo


# routes start from here

@auth_api.get("/check")
def check():
    return "auth service is up", 200

@auth_api.post("/login")
@cross_origin(supports_credentials=True)
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = authenticate_user(username, password)

    if not user:
        return AuthMessage.INVALID_CREDENTIALS, 401
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return jsonify({"token": access_token}), 200

def revoke_token(token: str):
    try: 
        payload = jwt.decode(token, ACTIVE_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        exp_ttl: timedelta = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc) - datetime.now(timezone.utc)

        if exp_ttl.total_seconds() > 0:
            r.setex(jti, math.ceil(exp_ttl.total_seconds()), b"True")
        
    except jwt.InvalidTokenError:
        return False
    return True

@auth_api.post("/revoke")
def revoke_jwt_token():

    header = request.headers.get("Authorization")

    if not header or not header.startswith("Bearer "):
        return AuthMessage.INVALID_TOKEN, 400

    token = header.split(" ")[1]

    revoke_token(token)
    return AuthMessage.TOKEN_REVOKED, 200

@auth_api.post("/user")
def add_user():
    data = request.get_json()
    try: 
        new_user = User(**data)
        new_user.password = generate_password_hash(new_user.password)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "User with similar username or email already exists"}), 400
    return f"an email has been sent to {new_user.email} for user {new_user.username}, please verify it", 201

@auth_api.get("/whoami")
@cross_origin(supports_credentials=True)
@auth_protected
def whoami(current_user):
    return current_user
    


