from fastapi import APIRouter, HTTPException, status
from src.Model.Administrator import Administrator
from src.Service.ItemService import ItemService
from src.Model.Item import Item, ItemCreate

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

item_service = ItemService()

@administrator_router.post("/Storage/Create_Item", status_code=status.HTTP_201_CREATED)
def Create_Item(item: ItemCreate, name_item: str, price : float, category : str, stock : int):
    try:
        new_item = item_service.create_item(name_item, price, category, stock)
        return {"message": "Item created successfully ✅", "item": new_item}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))

@administrator_router.patch("/Storage/Replemish_Item", status_code=status.HTTP_200_OK)
def Replemish_Item():
    pass
