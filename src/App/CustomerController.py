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
customer_service = CustomerService()


active_carts = {}


def get_cart_for_user(username: str):
    """Retourne le panier de l'utilisateur associé à son token"""
    return active_carts.get(username)


@customer_router.get("/Menu", status_code=status.HTTP_201_CREATED)
def View_menu():
    try:
        menu = customer_service.view_menu()
        print ("menu fetched:", menu)
        return menu
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))




@customer_router.get("/add to cart", status_code=status.HTTP_200_OK)
def order_items(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
    item: List[str] = Query(..., description="Item name"),
    quantities: List[int] = Query(..., description="Quantity for each item"),
):
    customer = get_user_from_credentials(credentials)
    username_customer = customer.username
    cart = get_cart_for_user(username_customer)
    if len(item) != len(quantities):
        return {"error": "Items and quantities must match"}
    try:
        cart = customer_service.add_item_cart(username_customer, cart, item= item, quantities = quantities)
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
