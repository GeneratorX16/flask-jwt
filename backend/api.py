from flask import jsonify, Blueprint, request
from auth import auth_protected
from db import User, Post, db
from flask_cors import cross_origin


content_api = Blueprint('api', __name__, url_prefix="/content")

@content_api.get("/users")
def get_user():
    return jsonify([{"username": user.username, "password": user.password, "email": user.email, "created_at": user.created_at} for user in User.query.all()])


# everything related with posts
@content_api.route("/check")
def check_app():
    return "success", 201

@content_api.get("/post")
@auth_protected
def get_posts(current_user: User):
    q = request.args.get('q')
    posts = Post.query

    if q:
        print("Applying query")
        posts = posts.filter(Post.title.ilike(f"%{q}%")).filter(Post.author_id == current_user.id)

    result = []
    for post in posts.all():
        result.append({"id": post.id, "title": post.title, "content": post.content, "created_at": post.created_at, "author": post.author.username})

    return jsonify(result)

@content_api.get("/post/<uuid:id>")
def get_post_by_id(id):
    post = Post.query.where(Post.id == id).all()

    if post:
        return jsonify(post)
    
    return "Resource not found", 404

@content_api.post("/post/create")
@cross_origin()
@auth_protected
def create_post(current_user: User):
    data = request.get_json()
    data["author_id"] = current_user.id
    new_post = Post(**data)
    try:
        db.session.add(new_post)
        db.session.commit()
    except Exception as e:
        print("Oops, something wnet wrong!")
        print(e)
        return "Error creating post, please try again in sometime", 500
    return "Post created successfully", 201

