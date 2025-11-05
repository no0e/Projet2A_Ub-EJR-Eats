from fastapi import APIRouter, HTTPException, status

from src.Model.Customer import Customer
from src.Service.CustomerService import CustomerServices

customer_router = APIRouter(prefix="/customer", tags=["Customer"])


@customer_router.get("/Menu", status_code=status.HTTP_201_CREATED)
def View_menu():
    customer_service = CustomerServices
    try:
        menu = customer_service.View_menu()
        return menu
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@customer_router.post("/Cart", status_code=status.HTTP_200_OK)
def Cart(name_item :str, number_item:int, new_number_item : int, validate : str, adress : str):
    customer_service = CustomerServices
    
    try:
        new_cart = customer_service.add_item_cart(cart, name_item, number_item)
        return new_cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        new_cart = customer_service.modify_cart(cart,  name_item, new_number_item)
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
