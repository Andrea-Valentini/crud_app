from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, resources

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(resources.router)
app.include_router(auth.router)
