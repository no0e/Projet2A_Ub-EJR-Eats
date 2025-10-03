from fastapi import APIRouter, HTTPException, status

from src.Model.Administrator import Administrator

administrator_router = APIRouter(prefix="/administrator", tags=["Administrator"])


@administrator_router.post("/Create_Accounts", status_code=status.HTTP_201_CREATED)
def Create_Accounts():
    pass


@administrator_router.patch("/Edit_Accounts", status_code=status.HTTP_200_OK)
def Edit_Accounts():
    pass


@administrator_router.patch("/Edit_Menu", status_code=status.HTTP_200_OK)
def Edit_Menu():
    pass


@administrator_router.get("/Storage/View", status_code=status.HTTP_200_OK)
def View_Storage():
    pass


@administrator_router.post("/Storage/Create_Item", status_code=status.HTTP_201_CREATED)
def Create_Item():
    pass


@administrator_router.patch("Storage/Replemish_Item", status_code=status.HTTP_200_OK)
def Replemish_Item():
    pass
