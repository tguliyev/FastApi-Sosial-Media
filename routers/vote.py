from models.user import UserModel
from models.vote import RequestVote
from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from services import auth_service
from services.database_service import connection, cursor, get_post_by_id


router = APIRouter(
    prefix='/votes',
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: RequestVote, current_user: UserModel = Depends(auth_service.get_current_user)):
    if get_post_by_id(vote.post_id) == None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

    cursor.execute("""SELECT * FROM votes WHERE user_id = %s AND post_id = %s""", (current_user.id, vote.post_id,))
    found_vote = cursor.fetchone()

    if (vote.direction == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")

        cursor.execute("""INSERT INTO votes (post_id, user_id) VALUES (%s, %s)""", (vote.post_id, current_user.id,))
        connection.commit()
        return {'message': 'vote added'}

    else:
        if found_vote == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        cursor.execute("""DELETE FROM votes WHERE user_id = %s AND post_id = %s""", (current_user.id, vote.post_id,))
        connection.commit()
        return {'message': 'vote deleted'}
