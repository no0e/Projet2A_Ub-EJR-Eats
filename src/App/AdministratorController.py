from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, status

from src.App.Auth_utils import require_account_type
from src.Model.Administrator import Administrator
from src.Model.APIUser import APIUser
from src.Model.Item import Item, ItemCreate
from src.Model.User import User
from src.Service.ItemService import ItemService
from src.Service.PasswordService import check_password_strength
from src.Service.DeliveryDriverService import DeliveryDriverService

from .init_app import admin_service, customer_service, jwt_service, user_repo, user_service

administrator_router = APIRouter(prefix="/administrator", tags=["Administrator"])

item_service = ItemService()
# remplacer cette ligne par :
# administrator_router = APIRouter(prefix="/administrator", tags=["Administrator"], dependencies=[Depends(require_account_type("Admin"))])
# pour limiter les actions aux admin


@administrator_router.post("/Create_Accounts", status_code=status.HTTP_201_CREATED)
def Create_Accounts(
    username: str,
    password: str,
    firstname: str,
    lastname: str,
    account_type: Literal["Administrator", "DeliveryDriver", "Customer"],
) -> APIUser:
    try:
        check_password_strength(password=password)
    except Exception:
        raise HTTPException(status_code=400, detail="Password too weak")
    try:
        user: User = admin_service.create_user(
            username=username, password=password, firstname=firstname, lastname=lastname, account_type=account_type
        )
    except Exception as error:
        raise HTTPException(status_code=409, detail=f"{error}")
    return APIUser(username=user.username, account_type=account_type)


@administrator_router.patch("/Edit_Accounts", status_code=status.HTTP_200_OK)
def Edit_Accounts(username: str, attribute: Literal["firstname", "lastname", "address", "vehicle"], new_value: str):
    if attribute == "address":
        if user_service.get_user(username).account_type != "Customer":
            raise ValueError("Only customers have an address.")
        customer_service.get_customer(username).address = new_value
    if attribute == "vehicle":
        if user_service.get_user(username).account_type != "DeliveryDriver":
            raise ValueError("Only delivery drivers have a vehicle.")
        driver_service.get_customer(username).address = new_value

@administrator_router.patch("/Edit_Menu", status_code=status.HTTP_200_OK)
def Edit_Menu():
    pass


@administrator_router.get("/Storage/View", status_code=status.HTTP_200_OK)
def View_Storage():
    pass


@administrator_router.post("/Storage/Create_Item", status_code=status.HTTP_201_CREATED)
def Create_Item(item: ItemCreate, name_item: str, price: float, category: str, stock: int):
    try:
        new_item = item_service.create_item(name_item, price, category, stock)
        return {"message": "Item created successfully ✅", "item": new_item}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@administrator_router.patch("/Storage/Change_Item", status_code=status.HTTP_200_OK)
def Change_Item(name_item):
    try:
        changes = item_service.change_availability(name_item)
        return changes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
