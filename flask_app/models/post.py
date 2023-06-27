from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

class Post:
    db = "dojo_wall"
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user']

    @classmethod
    def save(cls,data):
        print("in save")
        if not cls.validate_post(data):
            return False
        print("Data passed into create METHOD:", data)
        query = "INSERT INTO posts (content, users_id) VALUES (%(content)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def validate_post(cls,data):
        print("in validate")
        is_valid = True
        if len(data['content'])<1:
            print("invalid")
            flash("Post must contain at least one character.")
            is_valid = False
        print("valid")
        return is_valid
    
    @classmethod
    def delete_post(cls,post_id):
        query = "DELETE FROM posts WHERE id = (%(id)s);"
        connectToMySQL(cls.db).query_db(query, {"id": post_id})
        return post_id

    @classmethod
    def get_all(cls):
        query = """
        SELECT posts.id, posts.content, posts.created_at, posts.updated_at, users.id, users.first_name, users.last_name, users.email, users.created_at, users.updated_at FROM posts
        JOIN users ON posts.users_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_posts = []
        for row in results:
            posting_user = User({
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
                "password": ""
            })
            new_post = Post({
                "id": row["id"],
                "content": row["content"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user": posting_user
            })
            all_posts.append(new_post)
        return all_posts