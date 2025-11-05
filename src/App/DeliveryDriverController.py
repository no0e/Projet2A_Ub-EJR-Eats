from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.App.Auth_utils import get_user_from_credentials, require_account_type
from src.App.JWTBearer import JWTBearer
from src.DAO.DBConnector import DBConnector
from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.DAO.UserDAO import UserDAO
from src.Service.DeliveryDriverService import DeliveryDriverService
from src.Service.DeliveryService import DeliveryService

# Instanciation du connecteur et des DAOs
db_connector = DBConnector()
delivery_dao = DeliveryDAO(db_connector)
driver_dao = DeliveryDriverDAO(db_connector)
user_dao = UserDAO(db_connector)

# Services instanciés avec les bons DAOs
delivery_service = DeliveryService(delivery_dao)
driver_service = DeliveryDriverService(driver_dao, user_dao)

deliverydriver_router = APIRouter(
    prefix="/delivery_driver", tags=["DeliveryDriver"], dependencies=[Depends(require_account_type("Delivery_driver"))]
)


@deliverydriver_router.get("/Delivery", status_code=status.HTTP_200_OK)
def view_available_deliveries():
    """Liste toutes les livraisons non encore acceptées."""
    deliveries = delivery_service.get_available_deliveries()
    return {"available_deliveries": deliveries}


@deliverydriver_router.post(
    "/Delivery/accept/{id_delivery}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())]
)
def accept_delivery(
    id_delivery: int,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    """Permet au livreur connecté d'accepter une livraison."""
    username_driver = get_user_from_credentials(credentials).username
    vehicle_driver = get_user_from_credentials(credentials).vehicule
    try:
        result = delivery_service.accept_delivery(id_delivery, username_driver, vehicle_driver)
        return result
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@deliverydriver_router.patch("/Edit_Profile", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def edit_profile(
    vehicle: str = Query(..., description="Type of vehicle", enum=["driving", "walking", "bicycling"]),
    is_available: bool = Query(..., description="Driver availability"),
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())] = None,
):
    """Edit the vehicle type or availability status of the connected delivery driver."""

    driver = get_user_from_credentials(credentials)
    try:
        driver_dao.update(driver, vehicle, is_available)
    except Exception as error:
        raise HTTPException(status_code=403, detail=f"Error updating profile: {error}")

    return {
        "detail": "Profile updated successfully",
        "vehicle": vehicle,
        "is_available": is_available,
    }
