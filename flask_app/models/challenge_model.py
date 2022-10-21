from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask_app.models.users_model import User
class Challenge:
    TABLENAME='challenges'
    def __init__(self,data):
        self.id=data['id']
        self.challenger_id = data['challenger_id']
        self.challenged_id = data['challenged_id']
    @classmethod
    def challenge(cls,data):
        query = f"""INSERT INTO {cls.TABLENAME}(challenger_id,challenged_id)
        VALUES(%(challenger_id)s,%(challenged_id)s)"""
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def get_all(cls):
        query=f"""SELECT * FROM {cls.TABLENAME}
        JOIN users AS challenger ON challenger.id = challenger_id
        LEFT JOIN users ON users.id = challenged_id
        """
        results = connectToMySQL(DB).query_db(query)
        clist=[]
        for result in results:
            print(result)
            challenge = cls(result)
            challenger_data = {
                'id':result['id'],
                'first_name':result['first_name'],
                'last_name':result['last_name'],
                'persona':result['persona'],
                'rank':result['rank'],
                'park':result['park'],
                'email':result['email'],
                'password':result['password'],
                'created_at':result['created_at'],
                'updated_at':result['updated_at']
            }

            challenged_data={
                'id':result['users.id'],
                'first_name':result['users.first_name'],
                'last_name':result['users.last_name'],
                'persona':result['users.persona'],
                'rank':result['users.rank'],
                'park':result['users.park'],
                'email':result['users.email'],
                'password':result['users.password'],
                'created_at':result['users.created_at'],
                'updated_at':result['users.updated_at']
            }
            challenge.challenger=User(challenger_data)
            challenge.challenged=User(challenged_data)
            clist.append(challenge)
        return clist