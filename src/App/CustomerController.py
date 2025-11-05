from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.App.Auth_utils import get_user_from_credentials, require_account_type
from src.App.JWTBearer import JWTBearer
from src.Model.Customer import Customer
from src.Service.CustomerService import CustomerService

customer_router = APIRouter(prefix="/customer", tags=["Customer"])
# remplacer cette ligne par :
# customer_router = APIRouter(prefix="/customer", tags=["Customer"], dependencies=[Depends(require_account_type("Customer"))])
# pour limiter les actions aux customer
customer_service = CustomerService


active_carts = {}


def get_cart_for_user(username: str):
    """Retourne le panier de l'utilisateur associé à son token"""
    return active_carts.get(username)


@customer_router.get("/Menu", status_code=status.HTTP_201_CREATED)
def View_menu():
    try:
        menu = customer_service.View_menu()
        return menu
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@customer_router.post("/Cart", status_code=status.HTTP_200_OK)
def Cart(
    name_item: str,
    number_item: int,
    new_number_item: int,
    validate: str,
    adress: str,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    customer = get_user_from_credentials(credentials)
    username_customer = customer.username
    cart = get_cart_for_user(username_customer)
    try:
        new_cart = customer_service.add_item_cart(cart, name_item, number_item)
        return new_cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        new_cart = customer_service.modify_cart(cart, name_item, new_number_item)
        return new_cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        new_cart = customer_service.delete_item(cart, name_item)
        return new_cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        order = customer_service.validate_cart(cart, username_customer, validate, adress)
        return order
    


@customer_router.get("/add to cart")
def order_items(
    item: List[str] = Query(..., description="Item name"),
    quantity: List[int] = Query(..., description="Quantity for each item"),
):
    customer = get_user_from_credentials(credentials)
    username_customer = customer.username
    cart = get_cart_for_user(username_customer)
    if len(item) != len(quantity):
        return {"error": "Items and quantities must match"}
    try:
        cart = customer_service.add_item_cart(username_customer, cart, item, quantity)
        return cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@customer_router.post("/Order", status_code=status.HTTP_200_OK)
def View_order():
    pass


@customer_router.patch("/Edit_Profile", status_code=status.HTTP_200_OK)
def Edit_Profile():
    pass
