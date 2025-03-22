from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
import models, oauth2, schemas
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/like",
    tags=['Likes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(like: schemas.Like, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)) -> dict[str, Any]:

    if not db.query(models.Post).filter(models.Post.id == like.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such post found")

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    existing_like = like_query.first()

    if existing_like and like.direction == 0:
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Unliked the post"}
    if not existing_like and like.direction == 1:
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Liked the post"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not process your action")