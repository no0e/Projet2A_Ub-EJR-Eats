from fastapi import APIRouter, HTTPException, status

from src.Model.DeliveryDriver import DeliveryDriver

deliverydriver_router = APIRouter(prefix="/deliverydriver", tags=["DeliveryDriver"])


@deliverydriver_router.get("/Delivery", status_code=status.HTTP_200_OK)
def View_Available_Delivery():
    pass



@deliverydriver_router.patch("/Edit_Profile", status_code=status.HTTP_200_OK)
def Edit_Profile():
    pass

