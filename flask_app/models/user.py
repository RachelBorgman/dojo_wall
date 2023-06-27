from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
# r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

class User:
    db = "dojo_wall"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if len(user['email']) < 3:
            flash("Email must be at least 3 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['password2']:
            flash("Passwords do not match.")
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash('Password should have at least one number')
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash('Password should have at least one uppercase letter')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) < 3:
            flash("Login Email must be at least 3 characters.")
            is_valid = False
        if len(user['password']) < 3:
            flash("Login Password must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Login Invalid email address!")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result)<1:
            return False
        return cls(result[0])