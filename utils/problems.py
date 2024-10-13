from utils import DataBaseRegister


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
    def update_info_car(cls, 
                        car_id, 
                        description, 
                        date_start, 
                        date_finish):    
        with cls.conn.cursor() as cur:
            try:
                cur.execute('''
                    SELECT * FROM problems WHERE car_id = %s;
                ''', (car_id, ))
                problem = cur.fetchall()
                if problem:
                    cur.execute('''
                        UPDATE problems
                        SET description = %s, date_finish = %s
                        WHERE problems.car_id = %s;
                    ''', (description, date_finish, car_id))
                    print('машина есть в БД')
                else:
                    cur.execute('''
                        INSERT INTO problems (car_id, description, date_start, date_finish)
                        VALUES (%s, %s, %s, %s);
                    ''', (car_id, description, date_start, date_finish))
                    print('машины нет в БД')
            except Exception:
                cls.conn.rollback()
                return 'False'
            else:
                cls.conn.commit()
                return 'True'
            
    @classmethod
    def update_problem_information(cls, 
                                   problem_id, 
                                   title, 
                                   car_id, 
                                   description, 
                                   date_start, 
                                   date_finish):
        try:
            with cls.conn.cursor() as cur:
                cur.execute('''
                    UPDATE problems
                    SET car_id = %s, title = %s, description = %s, date_finish = %s
                    WHERE id = %s;
                ''', (car_id, title, description, date_finish, problem_id))
        except Exception as e:
            cls.conn.rollback()
            print(f'tut {e}')
            return 'False'
        else:
            cls.conn.commit()
            print('siud')
            return 'True'