from fastapi import FastAPI, HTTPException,status, Depends,Request
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from schemas import BaseResponse, CreateMenu, UpdateMenu
from fastapi.responses import JSONResponse
from menu_item_services import create_menu_item_services, get_all_menu_item_services, get_menu_item_by_id_services, update_menu_items_services,delete_menu_item_services
from fastapi.exceptions import RequestValidationError
app = FastAPI()


def converst(item):
    return{
        "id":item.id,
        "dish_code": item.dish_code,
        "dish_name":item.dish_name,
        "calorie_count":item.calorie_count,
        "price": item.price,
        "status":item.status
    }
@app.get("/test-connect")
def test_connect(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return{
            "thanh cong"
        }
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
def success_response(status_code:int, message: str,data: Any = None, error: Any = None, path: Any = str):
    return BaseResponse(
        status_code=status_code,
        message=message,
        data=data,
        error=error,
        timestamp= datetime.now().isoformat(),
        path=path
    )

def failed_response(status_code:int, message: str,data: Any = None, error: Any = None, path: Any = str):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode":status_code,
            "message":message,
            "data":data,
            "error":error,
            "timestamp":datetime.now().isoformat(),
            "path":path
        }
    )
@app.exception_handler(HTTPException)
def http_exception(request: Request, exc: HTTPException):
    return failed_response(
        status_code= exc.status_code,
        message="Failed",
        data=None,
        error=exc.detail,
        path=request.url.path
    )
@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    return failed_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Failed",
        data=None,
        error=str(exc),
        path=request.url.path
    )
@app.exception_handler(RequestValidationError)
def request_validation_handler(request: Request, exc: RequestValidationError):
    return failed_response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        message="Failed",
        data= None,
        error=exc.errors(),
        path=request.url.path
    )
@app.post("/menu-items")
def create_menu_item(request: Request, new_menu:CreateMenu, db: Session = Depends(get_db)):
    list = create_menu_item_services(db, new_menu)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Success",
        data= converst(list),
        error= None,
        path=request.url.path
    )
@app.get("/menu-items")
def get_all_menu_items(request: Request, db: Session = Depends(get_db)):
    list_menu_item = get_all_menu_item_services(db)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Success",
        data= [
            converst(i)
            for i in list_menu_item
        ],
        error=None,
        path=request.url.path
    )
@app.get("/menu-items/{item_id}")
def get_menu_item_by_id(request: Request, item_id: int, db: Session = Depends(get_db)):
    list = get_menu_item_by_id_services(db, item_id)

    if not list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found!"
        )
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Success",
        data= converst(list),
        error=None,
        path=request.url.path
    )
@app.put("/menu-items/{item_id}")
def update_menu_items(request: Request,update_menu: UpdateMenu, item_id:int,db:Session = Depends(get_db)):
    list_update = update_menu_items_services(db,item_id,update_menu)

    if not list_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Success",
        data= converst(list_update),
        error=None,
        path=request.url.path
    )
@app.delete("/menu-items/{item_id}")
def delete_menu_item(request:Request,item_id: int, db: Session = Depends(get_db)):
    menu_delete = delete_menu_item_services(db, item_id)

    if menu_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return success_response(
        status_code=status.HTTP_200_OK,
        message="Success",
        data= None,
        error=None,
        path=request.url.path
    )