from utils import DataBaseRegister

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
         with cls.conn.cursor() as cur:
            try:    
                cur.execute('''
                    UPDATE cars
                    SET active = CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM problems
                        WHERE problems.car_id = cars.id
                        )
                    THEN false
                    ELSE true
                    END;
                ''')
            except Exception:
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