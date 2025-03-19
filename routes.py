from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from requests import Session
import models
from database import get_db
from starlette.status import HTTP_303_SEE_OTHER
import schemas


# Initialize Router
router = APIRouter()

@router.post("/items/")
def add_item(item: schemas.Items, db: Session = Depends(get_db)):
    new_item = models.Items(name=item.name, description=item.description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Item added successfully!", "item": new_item}

@router.get("/items/")
def read_root(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Items).all()
    return items


@router.delete("/delete_all_items/")
def delete_all_items(db: Session = Depends(get_db)):
    db.query(models.Items).delete()
    db.commit()
    return {"message": "All items deleted successfully"}


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html",{"request": request,})


@router.delete("/delete_item/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Items).filter(models.Items.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

@router.put("/edit_item/{item_id}")
def edit_item(item_id: int, item: schemas.Items, db: Session = Depends(get_db)):
    existing_item = db.query(models.Items).filter(models.Items.id == item_id).first()
    old_item_name  = existing_item.name
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    existing_item.name = item.name
    existing_item.description = item.description
    db.commit()
    return {"message": "Item updated successfully", "old_item" : old_item_name,"updated_item":existing_item.name}

@router.get("/search/{name}")
def search_item(name: str, db: Session = Depends(get_db)):
    searched_item = db.query(models.Items).filter(models.Items.name == name or models.Items.name == name.capitalize()).all()
    
    if not searched_item:
        return {"message": "Item not found"}
    
    return searched_item 