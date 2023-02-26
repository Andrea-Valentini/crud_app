from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, oauth2, schemas, utils
from app.database import get_db

router = APIRouter(tags=["Authentication"])


@router.post(
    "/SignUp", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/SignIn", response_model=schemas.Token)
def signin(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    user.access_token = access_token
    db.commit()

    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/SignOut", status_code=status.HTTP_204_NO_CONTENT)
def signout(
    user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    user.access_token = None
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
