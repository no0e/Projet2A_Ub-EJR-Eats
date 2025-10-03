from fastapi import APIRouter, HTTPException, status

from src.Model.Driver import Driver

administrator_router = APIRouter(prefix="/administrator", tags=["Administrator"])


# @administrator_router.get("/", status_code=status.HTTP_200_OK)
