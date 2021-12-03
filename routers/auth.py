from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from services.database_service import cursor, connection
from models.token import Token
from models.user import UserModel
from services import hash_service, auth_service  


router = APIRouter(
    prefix='/login',
    tags=['Login']
)


@router.post('/', response_model=Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("""SELECT * FROM users WHERE email = %s""", (user_credential.username,))
    user = UserModel(**cursor.fetchone())

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    if not hash_service.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    access_token = auth_service.create_access_token(data={"user_id": user.id, "email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
