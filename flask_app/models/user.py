from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'solo_project'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = ['first_name']
        self.last_name = ['last_name']
        self.email = ['email']
        self.birthday = ['birthday']
        self.password = ['password']
        self.created_at = ['created_at']
        self.updated_at = ['updated_at']

    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users ( first_name, last_name, email, birthday, password, created_at, updated_at ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(birthday)s, %(password)s, NOW(), NOW() )"
        return connectToMySQL(User.db).query_db(query,data)
    
    @classmethod
    def get_user(cls,data):
        query = "SELECT FROM users WHERE id = %(id)s"
        results = connectToMySQL(User.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def edit(cls, data):
        query = " UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,birthday=%(birthday)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(User.db).query_db(query,data)
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(eml)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['eml']):
            flash("Invalid Email!!!","register")
            is_valid = False
        if len(user['fname']) < 3:
            flash("First name must be at least 2 characters","register")
            is_valid = False
        if len(user['lname']) < 3:
            flash("Last name must be at least 2 characters","register")
            is_valid = False
        if len(user['pswd']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid = False
        if user['pswd'] != user['con']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid