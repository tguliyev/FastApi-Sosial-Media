import time
import psycopg2
from fastapi import HTTPException, status
from psycopg2.extras import RealDictCursor
from app.config import settings


# Connecting to database
while True:
    try:
        connection = psycopg2.connect(
            host=settings.database_host,
            port=settings.database_port,
            database=settings.database_name, 
            user=settings.database_username, 
            password=settings.database_password, 
            cursor_factory=RealDictCursor)
        
        cursor = connection.cursor()
        print('Database connection established.')
        break
    except Exception as error:
        print('Database connection error.')
        print(error)
        time.sleep(3)


def get_user_by_id(id: int):
    cursor.execute("""SELECT * FROM users WHERE id = %s""", (id.__str__(),))
    data = cursor.fetchone()

    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f'user with id: {id} was not found')

    return data


def get_post_by_id(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id.__str__(),))
    data = cursor.fetchone()

    return data