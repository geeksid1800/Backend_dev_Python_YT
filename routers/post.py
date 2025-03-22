from typing import List, Optional
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy import func
from sqlalchemy.orm import Session

import models, schemas, oauth2
from database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model= List[schemas.LikeResponse])
def get_all_posts(db: Session = Depends(get_db), limit: int = 10, search: Optional[str] = ""):
    #Depends is a "Dependency Injection", what it means is that it calls the function get_db() and saves the return value to 'db'
    #limit is a query parameter, which is passed in the URL as ?limit=n

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

    posts_with_likes = db.query(models.Post, func.count(models.Like.post_id).label('likes')).join(models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit)
    #SQLAlchemy only provides option for left join, not right. The default join is 'left inner' (ie inner). We can modify to LEFT JOIN by using outerjoin() or join(isouter=True)

    return posts_with_likes.all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # Due to dependency injection of get_current_user, the function will be called and error thrown if we passed invalid/no JWT token in request header
    print(current_user)
    new_post = models.Post(user_id = current_user.id, **post.dict()) #Unpacks a dict into keyword arguments, so this line is shorthand for:
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #new_post is a Post object.
    db.add(new_post)
    db.commit()
    # print(f"The value of ID during commit is implicitly passed back as {new_post.id} to the python object")
    db.refresh(new_post) #Refresh the object to get the updated values, performs an implicit SELECT to reload the object from DB
    return new_post

@router.get("/{id}", response_model=schemas.LikeResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post_with_likes = db.query(models.Post, func.count(models.Like.post_id).label('likes')).join(models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post_with_likes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find a post with id {id}')
    return post_with_likes

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such post found")
    if current_user.id != post_query.first().user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such post found")
    if current_user.id != post_query.first().user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot edit this post")
    post_query.update(new_post.dict(), synchronize_session=False)
    #update() expects a dict of key-value pairs, whereas add() expects a models.Post object
    db.commit()
    return post_query.first()