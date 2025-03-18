from requests import Session
from routes import router
from fastapi import FastAPI
import database, models


app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Include the routes
app.include_router(router)




