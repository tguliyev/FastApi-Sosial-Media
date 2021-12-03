from typing import List, Optional
from models.user import UserModel
from services import auth_service
from fastapi.param_functions import Depends
from models.post import RequestPost, ResponsePost
from services.database_service import cursor, connection, get_user_by_id
from fastapi import Response, status, HTTPException, APIRouter


router = APIRouter(
    prefix = '/posts',
    tags=['Posts']
)


#Getting all posts
@router.get('/', response_model=List[ResponsePost])
def get_posts(current_user: UserModel = Depends(auth_service.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = "%"):
    cursor.execute("""SELECT posts.*, COUNT(votes.post_id) AS vote_count FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id WHERE content LIKE %s GROUP BY posts.id LIMIT %s OFFSET %s ROWS""", 
                    (search, limit.__str__(), skip.__str__()))
    
    data: List[dict] = cursor.fetchall()
    
    for post in data:
        post.update({'owner': get_user_by_id(post["user_id"])})

    return data


# Getting a single post by id
@router.get('/{id}', response_model=ResponsePost)
def get_post(id: int, current_user: UserModel = Depends(auth_service.get_current_user)):
    cursor.execute("""SELECT posts.*, COUNT(votes.post_id) AS vote_count FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id WHERE id=%s GROUP BY posts.id""", (id.__str__(),))
    data = cursor.fetchone()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

    data['owner'] = get_user_by_id(data["user_id"])
    return data


# Creating a new post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
def create_posts(new_post: RequestPost, current_user: UserModel = Depends(auth_service.get_current_user)):
    
    cursor.execute("""INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING *""", 
                (new_post.title, new_post.content, new_post.published, current_user.id))
    
    data = cursor.fetchone()
    connection.commit()
    data['owner'] = current_user
    return data


# Delete a post by id
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user: UserModel = Depends(auth_service.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id.__str__(),))
    data = cursor.fetchone()
    
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')

    if current_user.id != data['user_id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    cursor.execute("""DELETE FROM posts WHERE id = %s""", (id.__str__(),))
    connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post by id
@router.put('/{id}', response_model=ResponsePost)
def update_post(id: int, post: RequestPost, current_user: UserModel = Depends(auth_service.get_current_user)):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id.__str__(),))
    data = cursor.fetchone()    

    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

    if current_user.id != data['user_id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                (post.title, post.content, post.published, id.__str__(),))

    data = cursor.fetchone()
    connection.commit()
    return data