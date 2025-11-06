from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.App.Auth_utils import get_user_from_credentials, require_account_type
from src.App.JWTBearer import JWTBearer
from src.DAO.DeliveryDAO import DeliveryDAO
from src.Model.Administrator import Administrator
from src.Model.APIUser import APIUser
from src.Model.Item import Item, ItemCreate
from src.Model.User import User
from src.Service.PasswordService import check_password_strength

from .init_app import (
    admin_service,
    customer_repo,
    customer_service,
    db_connector,
    driver_repo,
    driver_service,
    google_map_service,
    item_service,
    jwt_service,
    user_repo,
    user_service,
)

administrator_router = APIRouter(prefix="/administrator", tags=["Administrator"])


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
        customer_repo.update_customer(username, new_value)
    if attribute == "vehicle":
        if user_service.get_user(username).account_type != "DeliveryDriver":
            raise ValueError("Only delivery drivers have a vehicle.")
        driver_repo.update_delivery_driver(username, vehicle=new_value)
    if attribute == "firstname":
        user_repo.update_user(username, firstname=new_value)
    if attribute == "lastname":
        user_repo.update_user(username, lastname=new_value)
    return {
        "detail": "Account updated successfully",
    }


@administrator_router.patch("/Edit_Menu", status_code=status.HTTP_200_OK)
def Edit_Menu():
    pass


@administrator_router.get("/Storage/View", status_code=status.HTTP_200_OK)
def View_Storage():
    try:
        storage = item_service.view_storage()
        print("Storage fetched:", storage)
        return storage
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@administrator_router.post("/Storage/Create_Item", status_code=status.HTTP_201_CREATED)
def Create_Item(
    item: ItemCreate,
    name_item: str,
    price: float,
    stock: int,
    category: str = Query(..., description="Type of item", enum=["starter", "main course", "dessert", "drink"]),
):
    try:
        new_item = item_service.create_item(name_item, price, category, stock)
        return {"message": "Item created successfully ", "item": new_item}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@administrator_router.patch("/Storage/Edit_Item", status_code=status.HTTP_200_OK)
def Edit_Item(
    name_item,
    new_name: str = None,
    change_availability: str = None,
    new_price: float = None,
    new_stock: int = None,
    new_category: str = Query(None, description="Type of item", enum=["starter", "main course", "dessert", "drink"]),
):
    try:
        if name_item and change_availability:
            changes = item_service.change_availability(name_item, change_availability)
            return changes
        if name_item and new_name:
            changes = item_service.change_name_item(name_item, new_name)
            return changes
        if name_item and new_price:
            changes = item_service.modify_price(name_item, new_price)
            return changes
        if name_item and new_stock:
            changes = item_service.modify_stock_item(name_item, new_stock)
            return changes
        if name_item and new_category:
            changes = item_service.modify_category_item(name_item, new_category)
            return changes

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@administrator_router.patch("/Storage/Delete_Item", status_code=status.HTTP_200_OK)
def Delete_Item(name_item):
    try:
        item_deleted = item_service.delete_item(name_item)
        return item_deleted
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@administrator_router.patch("/Storage/Edit_Profile", status_code=status.HTTP_200_OK)
def edit_Profile(
    firstname: Optional[str] = Query(None, description="First name"),
    lastname: Optional[str] = Query(None, description="Last name"),
    password: Optional[str] = Query(None, description="Password"),
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())] = None,
):
    """Edit the attributes of the connected administrator."""

    username = get_user_from_credentials(credentials).username

    try:
        user_service.update_user(username, firstname, lastname, password)
    except Exception as error:
        raise HTTPException(status_code=403, detail=f"Error updating profile: {error}")

    return {
        "detail": "Profile updated successfully",
        "firstname": firstname,
        "lastname": lastname,
        "password": password,
    }
