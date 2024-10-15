from psycopg2 import connect
from psycopg2.errors import Error
from settings import settings



class DataBaseRegister:
    conn = connect(settings.DATABASE_URL)
    
    @classmethod
    def create_tables(cls):
        with cls.conn.cursor() as cur:
            try:
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
                        car_number VARCHAR(16) NOT NULL UNIQUE,
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