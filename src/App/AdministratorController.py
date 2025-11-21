from __future__ import annotations

from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.App.Auth_utils import get_user_from_credentials, require_account_type
from src.App.JWTBearer import JWTBearer
from src.Model.APIUser import APIUser
from src.Model.Item import Item
from src.Model.User import User
from src.Service.PasswordService import check_password_strength

from .init_app import (
    admin_service,
    customer_repo,
    driver_repo,
    google_map_service,
    item_repo,
    item_service,
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
    """Function that calls the User creation function from an administrator point of view.

    Parameters
    ----------
    username: str
        user's username
    password: str
        user's password
    firstname: str
        user's firstname
    lastname: str
        user's lastname
    account_type: str
        user's account type


    Returns
    -------
    APIUser
        Returns the APIUser that has been created.
    """
    try:
        check_password_strength(password=password)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Password too weak") from e
    try:
        user: User = admin_service.create_user(
            username=username.lower(),
            password=password,
            firstname=firstname,
            lastname=lastname,
            account_type=account_type,
        )
    except Exception as error:
        raise HTTPException(status_code=409, detail=f"{error}") from error
    return APIUser(username=user.username, account_type=account_type)


@administrator_router.patch("/Edit_Accounts", status_code=status.HTTP_200_OK)
def Edit_Accounts(
    username: str, attribute: Literal["firstname", "lastname", "address", "vehicle"], new_value: str
) -> dict:
    """Function that modify a user's attribute by calling the different DAO's methods.

    Parameters
    ----------
    username: str
        user's username
    attribute: str
        user's attribute to modify
    new_value: str
        user's new value for the attribute selected


    Returns
    -------
    dict
        Returns a dict that informs the user the modification has been done.
    """
    if attribute == "address":
        if user_service.get_user(username).account_type != "Customer":
            raise ValueError("Only customers have an address.")
        google_map_service.geocoding_address(new_value)
        customer_repo.update_customer(username, new_value)
    if attribute == "vehicle":
        if user_service.get_user(username).account_type != "DeliveryDriver":
            raise ValueError("Only delivery drivers have a vehicle.")
        if new_value not in ("walking", "cycling", "driving"):
            raise ValueError("Vehicle not accepted. Values accepted : 'walking', 'cycling' or 'driving'.")
        driver_repo.update_delivery_driver(username, vehicle=new_value)
    if attribute == "firstname":
        user_repo.update_user(username, firstname=new_value)
    if attribute == "lastname":
        user_repo.update_user(username, lastname=new_value)
    return {
        "detail": "Account updated successfully",
    }


@administrator_router.delete("/Storage/Delete_User", status_code=status.HTTP_200_OK)
def Delete_User(username) -> bool:
    """Function that calls the function to delete a User.

    Parameters
    -------
    username: str
        username of the user

    Returns
    -------
    bool
        True the User that has been deleted.
        False otherwise
    """
    try:
        user_deleted = administrator_router_service.delete_user(username)
        return user_deleted
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@administrator_router.get("/Storage/View", status_code=status.HTTP_200_OK)
def View_Storage() -> dict:
    """Function that print the whole set of items and their quantities to the user.

    Returns
    -------
    dict
        Returns a dict containing an item's name associated with its quantity in storage.
    """
    try:
        storage = item_service.view_storage()
        print("Storage fetched:", storage)
        return storage
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@administrator_router.post("/Storage/Create_Item", status_code=status.HTTP_201_CREATED)
def Create_Item(
    name_item: str,
    price: float,
    stock: int,
    category: str = Query(..., description="Type of item", enum=["starter", "main course", "dessert", "drink"]),
) -> dict:
    """Function that calls the function to create an item.

    Parameters
    -------
    name_item: str
        item's name
    price: float
        item's price
    stock: int
        item's quantity available
    category: str
        item's category

    Returns
    -------
    dict
        Returns a dict that informs the user the item has been created.
    """
    try:
        new_item = item_service.create_item(name_item, int(price * 100), category, stock)
        return {"message": "Item created successfully ", "item": new_item}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@administrator_router.patch("/Storage/Edit_Item", status_code=status.HTTP_200_OK)
def Edit_Item(
    name_item,
    new_name: str = None,
    new_price: float = None,
    new_category: str = Query(None, description="Type of item", enum=["starter", "main course", "dessert", "drink"]),
    new_stock: int = None,
    availability: bool = Query(None, description="Is the item available ?", enum=[True, False]),
) -> dict:
    """Function that calls the function to update an item.

    Parameters
    -------
    name_item: str
        item's name
    new_name: str
        item's new name, by default None
    new_price: float
        item's new price, by default None
    new_category: str
        item's new category, by default None
    new_stock: int
        item's new quantity, by default None
    availability: bool
        item's availability, by default None

    Returns
    -------
    dict
        Returns a dict that informs the user the item has been updated.
    """
    try:
        item_service.update(name_item, new_name, int(new_price * 100), new_category, new_stock, availability)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if new_name is None:
        item = item_repo.find_item_by_name(name_item)
    else:
        item = item_repo.find_item_by_name(new_name)
    return {
        "detail": "Item updated successfully",
        "name_item": item.name_item,
        "price": round(item.price / 100, 2),
        "category": item.category,
        "stock": item.stock,
        "availability": item.exposed,
    }


@administrator_router.delete("/Storage/Delete_Item", status_code=status.HTTP_200_OK)
def Delete_Item(name_item) -> Item:
    """Function that calls the function to delete an item.

    Parameters
    -------
    name_item: str
        item's name

    Returns
    -------
    Item
        Returns the Item that has been deleted.
    """
    try:
        item_deleted = item_service.delete_item(name_item)
        return item_deleted
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@administrator_router.patch("/Storage/Edit_Profile", status_code=status.HTTP_200_OK)
def edit_Profile(
    firstname: Optional[str] = Query(None, description="First name"),
    lastname: Optional[str] = Query(None, description="Last name"),
    password: Optional[str] = Query(None, description="Password"),
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())] = None,
) -> dict:
    """Function that calls the function to update the user's own profile

    Parameters
    -------
    firstname: str
        admin's new firstname, by default None
    lastname: str
        admin's new lastname, by default None
    password: str
        admin's new password, by default None
    credentials: HTTPAuthorizationCredentials
        admin's credentials, by default None

    Returns
    -------
    dict
        Returns the dict summarising all the administrator's new information.
    """

    username = get_user_from_credentials(credentials).username

    try:
        user_service.update_user(username, firstname, lastname, password)
    except Exception as error:
        raise HTTPException(status_code=403, detail=f"Error updating profile: {error}") from error

    return {
        "detail": "Profile updated successfully",
        "firstname": firstname,
        "lastname": lastname,
        "password": password,
    }
