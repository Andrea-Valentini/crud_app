from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(tags=["Resources"])


@router.get("/GetOne/id={id}", response_model=schemas.Resource)
def get_one(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    """
    Retrieves all the resources in the database
    """
    resource = db.query(models.Resource).filter(models.Resource.id == id).first()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"resource with ID {id} was not found",
        )
    return resource


@router.get("/GetList", response_model=List[schemas.Resource])
def get_list(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    """
    Retrieves the indicated resource in the database
    Params: id
    """
    resources = db.query(models.Resource).order_by("id").all()
    return resources


@router.post(
    "/CreateOne", status_code=status.HTTP_201_CREATED, response_model=schemas.Resource
)
def create(
    resource: schemas.ResourceCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """
    Creates a resource in the database
    """
    new_resource = models.Resource(**resource.dict())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


@router.delete("/DeleteOne/id={id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    """
    Deletes the indicated resource in the database
    """
    resource_query = db.query(models.Resource).filter(models.Resource.id == id)

    if not resource_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"resource with ID {id} was not found",
        )

    resource_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/UpdateOne/id={id}", response_model=schemas.Resource)
def update(
    id: int,
    resource: schemas.ResourceUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """
    Update the indicated resource in the database
    """
    resource_query = db.query(models.Resource).filter(models.Resource.id == id)

    resource_to_update = resource_query.first()
    if resource_to_update == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"resource with ID {id} was not found",
        )

    resource_query.update(values=resource.dict(), synchronize_session=False)
    db.commit()
    return resource_query.first()


@router.get("/items", response_model=List[schemas.Resource])
def read_items(
    created_at__gte: str,
    created_at__lte: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """
    Retrieves resources having a creation date between created_at__gte and created_at__lte params
    """

    def str_to_datetime(date):
        try:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            return date
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid datetime format for parameter {date}: {str(error)}",
            )

    created_at__gte = str_to_datetime(created_at__gte)
    created_at__lte = str_to_datetime(created_at__lte)

    if created_at__gte <= created_at__lte:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"created_at_gte shall be higher than created_at__lte",
        )
    resources = (
        db.query(models.Resource)
        .filter(
            models.Resource.created_at > created_at__lte,
            models.Resource.created_at < created_at__gte,
        )
        .all()
    )

    return resources
