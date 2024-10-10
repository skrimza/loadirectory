from database import DataBaseRegister

from psycopg2.errors import UniqueViolation, InFailedSqlTransaction
from werkzeug.security import generate_password_hash, check_password_hash

class Profile(DataBaseRegister):
    
    
    def __init__(self, 
                 name, 
                 lastname, 
                 email, 
                 password, 
                 conn=DataBaseRegister.conn):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password
        self.conn = conn
    
    
    def new_user(self):
        response_text = None
        hashed_password = generate_password_hash(self.password)
        try:
            with self.conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO users (name, lastname, email, password)
                    VALUES (%s, %s, %s, %s);
                ''', (self.name, self.lastname, self.email, hashed_password))
        except UniqueViolation as e:
            response_text = {'error': 'Такой пользователь уже существует', 
                             'message': str(e)}
        else:
            self.conn.commit()
            response_text = {'text': 'Регистрация успешно пройдена, теперь авторизуйтесь', 
                             'name': self.name} 
        return response_text

    
    def login_user(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT name, email, password FROM users
                WHERE email= %s;
            ''', (self.email, ))
            user_data = cur.fetchone()
            if user_data is None:
                return {'error': 'такого пользователя не существует'}
            else:
                if check_password_hash(user_data[2], self.password):
                    return {'message': 'Добро пожаловать', 'name': user_data[0]}
                else:
                    print(user_data[2], )
                    return {'error': 'пароль неправильный, попробуйте еще раз'}
    
    
    @classmethod
    def get_all_users(cls):
        
        with cls.conn.cursor() as cur:
            try:
                cur.execute('''
                    SELECT id, name, lastname FROM users;
                ''')
            except InFailedSqlTransaction:
                cls.conn.rollback()
            else:
                return cur.fetchall()