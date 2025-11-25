from flask import jsonify, Blueprint, request
from sqlalchemy.exc import IntegrityError
from auth import auth_protected, generate_password_hash
from db import User, Post, db


content_api = Blueprint('api', __name__)

@content_api.get("/users")
def get_user():
    return jsonify([{"username": user.username, "password": user.password, "email": user.email, "created_at": user.created_at} for user in User.query.all()])

@content_api.post("/user")
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


# everything related with posts
@content_api.route("/check")
def check_app():
    return "success", 201

@content_api.get("/post")
@auth_protected
def get_posts():
    q = request.args.get('q')
    posts = Post.query
    print("Query found: " + (q or "e"))
    if q:
        print("Applying query")
        posts = posts.filter(Post.title.ilike(f"%{q}%"))

    result = []
    for post in posts.all():
        result.append({"id": post.id, "title": post.title, "content": post.content, "created_at": post.created_at})

    return jsonify(result)

@content_api.get("/post/<uuid:id>")
def get_post_by_id(id):
    post = Post.query.where(Post.id == id).all()

    if post:
        return jsonify(post)
    
    return "Resource not found", 404

@content_api.post("/post/create")
def create_post():
    data = request.get_json()
    new_post = Post(**data)
    try:
        db.session.add(new_post)
        db.session.commit()
    except Exception as e:
        print("Oops, something wnet wrong!")
        print(e)
        return "Error creating post, please try again in sometime", 500
    return "Post created successfully", 201

