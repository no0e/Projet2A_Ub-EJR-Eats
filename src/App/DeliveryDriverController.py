from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

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

# Router
deliverydriver_router = APIRouter(prefix="/delivery_driver", tags=["DeliveryDriver"])


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
    username_driver = credentials.subject  # fourni par JWTBearer
    try:
        result = delivery_service.accept_delivery(id_delivery, username_driver)
        return result
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@deliverydriver_router.patch("/Edit_Profile", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def edit_profile(
    vehicule: str,
    is_available: bool,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    """Modifie le type de véhicule ou la disponibilité du livreur connecté."""
    allowed_vehicles = ["foot", "bike", "car"]
    if vehicule.lower() not in allowed_vehicles:
        raise HTTPException(status_code=400, detail=f"Invalid vehicle type. Must be one of {allowed_vehicles}")

    username_driver = credentials.subject  # récupéré via JWT
    try:
        driver_service.update_vehicle(username_driver, vehicule.lower())
        driver_service.update_availiability(username_driver, is_available)
    except Exception as error:
        raise HTTPException(status_code=403, detail=f"Error updating profile: {error}")

    return {
        "detail": "Profile updated successfully",
        "vehicle": vehicule.lower(),
        "is_available": is_available,
    }
