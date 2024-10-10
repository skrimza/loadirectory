from psycopg2 import connect
from psycopg2.errors import Error, UniqueViolation, InFailedSqlTransaction
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class DataBaseRegister:
    conn = connect('postgresql://skrim:skrimza@localhost:5432/catalogy')
    
    @classmethod
    def create_tables(cls):
        try:
            with cls.conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE if NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(64) NOT NULL,
                        lastname VARCHAR(64) NOT NULL,
                        email VARCHAR(64) NOT NULL UNIQUE,
                        password VARCHAR NOT NULL
                    );
                ''')
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS cars(
                        id SERIAL PRIMARY KEY,
                        car_name VARCHAR(64) NOT NULL,
                        car_number VARCHAR(10) NOT NULL UNIQUE,
                        load_capacity DECIMAL(5, 3),
                        active BOOLEAN DEFAULT true,
                        date_publish TIMESTAMP DEFAULT now(),
                        user_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE               
                    );
                ''')
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS problems(
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(24),
                        description TEXT NOT NULL,
                        car_id INTEGER NOT NULL,
                        date_start TIMESTAMP DEFAULT now(),
                        date_finish TIMESTAMP DEFAULT now(),
                        FOREIGN KEY (car_id) REFERENCES cars(id)
                    )
                ''')
        except Error:
            cls.conn.rollback()
        else:
            cls.conn.commit()


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
        
    
        
        
class Cars(DataBaseRegister):
    
    
    def __init__(self, 
                 car_name, 
                 car_number, 
                 load_capacity, 
                 date_publish, 
                 user_id, 
                 conn=DataBaseRegister.conn):
        self.car_name = car_name
        self.car_number = car_number
        self.load_capacity = load_capacity
        self.date_publish = date_publish
        self.user_id = user_id
        self.conn = conn
        
        
    def add_new_car(self):
        with self.conn.cursor() as cur:
            try:
                cur.execute('''
                    INSERT INTO cars (car_name, car_number, load_capacity, date_publish, user_id)
                    VALUES (%s, %s, %s, %s, %s);
                ''', (self.car_name, self.car_number, self.load_capacity, self.date_publish, self.user_id))
            except Exception:
                return 'Недостаточно данных, попробуйте ввести еще раз'
            else:
                self.conn.commit()
        return 'Данные успешно сохранены'
    
    @classmethod   
    def get_all_cars(cls):
        with cls.conn.cursor() as cur:
            cur.execute('''
                SELECT cars.id, cars.car_name, cars.car_number, cars.load_capacity, cars.active, cars.date_publish, users.name, users.lastname FROM cars
                JOIN users ON cars.user_id = users.id;
            ''')
            return cur.fetchall()
    
    @classmethod
    def update_active_car(cls):
        try:
            with cls.conn.cursor() as cur:
                cur.execute('''
                    UPDATE cars
                    SET active = NOT EXISTS (
                        SELECT 1
                        FROM problems
                        WHERE problems.car_id = cars.id
                    );
                ''')
        except InFailedSqlTransaction:
            cls.conn.rollback()
        else:
            cls.conn.commit()
            
    @classmethod
    def delete_car(cls, car_id):
        with cls.conn.cursor() as cur:
            try:
                cur.execute('''
                    DELETE FROM cars WHERE cars.id = %s;
                ''', (car_id, ))
            except Exception:
                cls.conn.rollback()
                return 'False'
            else:
                cls.conn.commit()
                return 'True'
        


class Problems(DataBaseRegister):

   
    def __init__(self, 
                 title, 
                 description, 
                 car_id, 
                 date_start, 
                 date_finish,
                 conn=DataBaseRegister.conn):
        self.title = title
        self.description = description
        self.car_id = car_id
        self.date_start = date_start
        self.date_finish = date_finish
        self.conn = conn
     
        
    def add_new_problem(self):
        with self.conn.cursor() as cur:
            try:
                cur.execute('''
                    INSERT INTO problems (title, description, car_id, date_start, date_finish)
                    VALUES (%s, %s, %s, %s, %s);
                ''', (self.title, self.description, self.car_id, self.date_start, self.date_finish))
            except Exception as e:
                return f'Недостаточно данных, попробуйте ввести еще раз {e}'
            else:
                self.conn.commit()
                return 'Данные успешно сохранены'
    
    
    @classmethod        
    def get_all_problems(cls):
        with cls.conn.cursor() as cur:
            cur.execute('''
                SELECT problems.id, problems.title, problems.description, problems.date_start, problems.date_finish, cars.car_number FROM problems
                JOIN cars ON problems.car_id = cars.id;
            ''')
            return cur.fetchall()
    
    
    @classmethod
    def delete_problem(cls, problem_id):
        with cls.conn.cursor() as cur:
            try:
                cur.execute('''
                    DELETE FROM problems WHERE problems.id = %s;
                ''', (problem_id, ))
            except Exception:
                cls.conn.rollback()
                return 'False'
            else:
                cls.conn.commit()
                return 'True'
        
            
    @classmethod
    def update_info_car(cls, car_id, description, date_start, date_finish):
        try:    
            with cls.conn.cursor() as cur:
                cur.execute('''
                    SELECT * FROM problems WHERE car_id = %s;
                ''', (car_id))
                if cur.fetchall():
                    cur.execute('''
                        UPDATE problems 
                        SET description = %s, date_finish = %s
                        WHERE problems.car_id = %s
                    ''', (description, date_finish, car_id))
                else:
                    cur.execute('''
                        INSERT INTO problems car_id, description, date_start, date_finish
                        VALUES (%s, %s, %s, %s);
                    ''', (car_id, description, date_start, date_finish))
        except Exception:
            cls.conn.rollback()
            return 'False'
        else:
            cls.conn.commit()
            return 'True'
            