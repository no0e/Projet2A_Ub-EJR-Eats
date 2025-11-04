from fastapi import APIRouter, HTTPException, status
from src.Model.Administrator import Administrator
from src.Service.ItemService import ItemService
from src.Model.Item import Item

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
def Create_Item(item: Item):
    try:
        # Appel du service métier pour créer un nouvel item
        new_item = item_service.create_item(
            name=item.name,
            price=item.price,
            category=item.category,
            stock=item.stock,
            exposed=item.exposed,
        )

        # FastAPI sait convertir les objets Pydantic en JSON automatiquement
        return {
            "message": "Item created successfully ✅",
            "item": new_item,
        }

    except (TypeError, ValueError) as e:
        # Si une erreur de validation survient
        raise HTTPException(status_code=400, detail=str(e))

@administrator_router.patch("Storage/Replemish_Item", status_code=status.HTTP_200_OK)
def Replemish_Item():
    pass
