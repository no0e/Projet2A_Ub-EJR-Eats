from fastapi import APIRouter, HTTPException, status

from src.Model.Customer import Customer

customer_router = APIRouter(prefix="/customer", tags=["Customer"])


@customer_router.get("/Menu", status_code=status.HTTP_201_CREATED)
def View_menu():
    pass


@customer_router.post("/Order", status_code=status.HTTP_200_OK)
def View_order():
    pass


@customer_router.patch("/Edit_Profile", status_code=status.HTTP_200_OK)
def Edit_Profile():
    pass
