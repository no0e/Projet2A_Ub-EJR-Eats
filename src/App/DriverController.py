from fastapi import APIRouter, HTTPException, status

from src.Model.Driver import Driver

driver_router = APIRouter(prefix="/driver", tags=["Driver"])


#@driver_router.post("/", status_code=status.HTTP_200_OK)