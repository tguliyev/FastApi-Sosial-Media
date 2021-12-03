from services.hash_service import hash
from models.user import RequestUser, ResponseUser
from services.database_service import cursor, connection, get_user_by_id
from fastapi import status, HTTPException, APIRouter


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


#Creating user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
def create_user(new_user: RequestUser):
    # Hash the password
    hash_password = hash(new_user.password)

    cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *""", (new_user.email, hash_password))

    data = cursor.fetchone()
    connection.commit()
    return data


# Getting a single user by id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ResponseUser)
def get_user(id: int):

    return get_user_by_id(id)