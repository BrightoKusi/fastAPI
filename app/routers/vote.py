from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from .. import schemas, database, models, oath2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=['VOTE'])



@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: schemas.TokenData = Depends(oath2.get_current_user)):  
    # Ensure user_id is extracted from current_user.id
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Successfully created vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Successfully deleted vote"}
