import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB,bcrypt
from flask import flash,session
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')

class User:
    TABLENAME = 'users'
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name = data['last_name']
        self.persona = data['persona']
        self.rank=data['rank']
        self.park= data['park']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def create(cls,form_data):
        data = {
            **form_data,
            'password':bcrypt.generate_password_hash(form_data['password']),
            'rank': cls.get_rank()+1}
        query = f"""INSERT INTO {cls.TABLENAME}(first_name,last_name,persona,park,`rank`,email,password)
        VALUES(%(first_name)s,%(last_name)s,%(persona)s,%(park)s,%(rank)s,%(email)s,%(password)s)"""
        return connectToMySQL(DB).query_db(query,data)

    @classmethod 
    def get_by_id(cls,id):
        data ={ 'id':id }
        query = f"SELECT * FROM {cls.TABLENAME} WHERE id = %(id)s"
        result= connectToMySQL(DB).query_db(query,data)
        if result:
            return cls(result[0])
    @classmethod
    def get_rank(cls):
        query = f"SELECT users.rank FROM {cls.TABLENAME} ORDER BY users.rank DESC LIMIT 1"
        result= connectToMySQL(DB).query_db(query)
        if result:
            return result[0]['rank']
    @classmethod
    def get_by_email(cls,data):
        query = f"SELECT * FROM {cls.TABLENAME} WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod 
    def get_all_order_by_rank(cls):
        query = f"SELECT * FROM {cls.TABLENAME} ORDER BY `rank`"
        results= connectToMySQL(DB).query_db(query)
        if results:
            listUsers=[]
            for result in results:
                listUsers.append(cls(result))
            return listUsers
    @classmethod 
    def get_5_order_by_rank(cls,rank):
        data={
            'rank':rank
        }
        query = f"SELECT * FROM {cls.TABLENAME} WHERE `rank`< %(rank)s ORDER BY `rank` LIMIT 5 "
        results= connectToMySQL(DB).query_db(query,data)
        listUsers=[]
        for result in results:
            listUsers.append(cls(result))
        return listUsers

    @staticmethod
    def validate_login(data):
        is_valid = True
        user_in_db = User.get_by_email(data)
        if not user_in_db:
            flash("Invalid Email/Password")
            return False
        if not bcrypt.check_password_hash(user_in_db.password, data['password']):
            flash("Invalid Email/Password")
            is_valid = False
        if is_valid:
            session['user_id'] = user_in_db.id
            session['persona'] = user_in_db.persona
        return is_valid

    @staticmethod
    def user_is_valid(user):
        is_valid = True
        result= User.get_by_email(user)
        if  result:
            flash('Email already in use')
            is_valid = False
        if len(user['first_name'])<2:
            is_valid = False
            flash('First Name must be at least 2 characters long ')
        if len(user['last_name'])<2:
            is_valid = False
            flash('Last Name must be at least 2 characters long ')
        if len(user['persona'])<2:
            is_valid = False
            flash('Persona must be at least 2 characters long ')
        if not EMAIL_REGEX.match(user['email']):
            flash('invalid email')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash('Password must be 8 characters long  and contain one  Lowercase ,Capital, number, and special character')
        if not user['password'] == user['confirm']:
            flash('Confirm password does not match')
            is_valid = False
        return is_valid