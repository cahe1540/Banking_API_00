from psycopg2 import connect
from psycopg2._psycopg import OperationalError
import os


def create_connection():
    try:
        conn = connect(
            host= os.environ.get('HOST'),
            database= os.environ.get('DB_NAME'),
            user= os.environ.get('DB_USERNAME'),
            password= os.environ.get('DB_PASSWORD'),
            port= os.environ.get('PORT')
        )
        print('successfully connected to database...')
        return conn
    except OperationalError as e:
        print(e)


connection = create_connection()