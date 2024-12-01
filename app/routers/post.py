from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit:int = 10, skip:int= 0, search: Optional[str] =""):
    # cursor.execute("""SELECT * FROM  posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # Convert results into a list of PostOut schemas
    posts_with_votes = [
        schemas.PostOut(
            post=schemas.Post.from_orm(row[0]),  # Convert SQLAlchemy Post to Pydantic Post
            votes=row[1]  # The vote count
        )
        for row in results
    ]
    
    return posts_with_votes


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # Query for the post and count the votes for the specific post by its id
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
               .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
               .group_by(models.Post.id) \
               .filter(models.Post.id == id) \
               .first()  # We expect only a single result here
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} not found")
    
    # result is a tuple (Post, votes_count)
    post = schemas.PostOut(
        post=schemas.Post.from_orm(result[0]),  # Convert SQLAlchemy Post to Pydantic Post
        votes=result[1]  # The vote count
    )
    
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post with id:{id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post with id:{id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()