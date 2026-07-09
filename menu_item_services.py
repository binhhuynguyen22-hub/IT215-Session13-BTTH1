from sqlalchemy.orm import Session
from schemas import CreateMenu, UpdateMenu
from model import MenuItem

def create_menu_item_services(db:Session,new_menu:CreateMenu):
    new_menu = MenuItem(**new_menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)

    return new_menu
def get_all_menu_item_services(db:Session):
    list = db.query(MenuItem).all()
    return list
def get_menu_item_by_id_services(db:Session, id: int):
    check = db.query(MenuItem).filter(MenuItem.id == id).first()

    if check is None:
        return None
    return check
def update_menu_items_services(db: Session, id :int, update_menu:UpdateMenu):
    update = db.query(MenuItem).filter(MenuItem.id == id).first()
    
    if update is None:
        return None
    for key, value in update_menu.model_dump().items():
        setattr(update,key,value)
        db.commit()
        db.refresh(update)
    return update
def delete_menu_item_services(db:Session, id:int):
    delete = db.query(MenuItem).filter(MenuItem.id == id).first()

    menu_delete = delete

    if delete is None:
        return None
    db.delete(delete)
    db.commit()
    return menu_delete