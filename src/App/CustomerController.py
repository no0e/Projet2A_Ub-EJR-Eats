from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials

from src.App.Auth_utils import get_user_from_credentials, require_account_type
from src.App.JWTBearer import JWTBearer

from src.Model.Customer import Customer
from src.Service.CustomerService import CustomerServices

customer_router = APIRouter(prefix="/customer", tags=["Customer"])
# remplacer cette ligne par :
# customer_router = APIRouter(prefix="/customer", tags=["Customer"], dependencies=[Depends(require_account_type("Customer"))])
# pour limiter les actions aux customer
customer_service = CustomerServices

def create_cart():
    

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
def Cart(name_item: str, number_item: int, new_number_item: int, validate: str, adress: str, credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]):
    customer = get_user_from_credentials(credentials)
    username_customer = customer.username
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
