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

# Initialize Jinja2 template engine
templates = Jinja2Templates(directory="templates")

@router.post("/items/")
def add_item(name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    new_item = models.Items(name=name, description=description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    print({"message": "Item added successfully!"})
    return RedirectResponse(url="/items",status_code=HTTP_303_SEE_OTHER)


@router.get("/items/")
def read_root(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Items).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


@router.delete("/delete_all_items/")
def delete_all_items(db: Session = Depends(get_db)):
    db.query(models.Items).delete()
    db.commit()
    return {"message": "All items deleted successfully"}


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html",{"request": request,})

@router.get("/items_list/")
def item_list(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Items).all()
    return templates.TemplateResponse("items.html", {"request": request, "items": items})

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
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    existing_item.name = item.name
    existing_item.description = item.description
    db.commit()
    return {"message": "Item updated successfully"}