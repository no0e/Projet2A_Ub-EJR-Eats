from fastapi import APIRouter, HTTPException, status

from src.Model.Customer import Customer

customer_router = APIRouter(prefix="/customer", tags=["Customer"])


#@customer_router.get("/", status_code=status.HTTP_200_OK)