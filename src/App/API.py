import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.DAO.DBConnector import DBConnector

from .AdministratorController import administrator_router
from .CustomerController import customer_router
from .DeliveryDriverController import deliverydriver_router
from .UserController import user_router


def run_app(reset_db=False):

    app = FastAPI(title="Ub’EJR Eats", 
    description=f"This API allow you to connect as a customer, a delivery driver or an administrator to the ENSAI Junior Restaurant.<br>"
                f"As a customer you can create a cart by choosing items from the menu. You can then order it.<br>"
                f"As a delivery driver you can see the pendant orders and accept it. You will be provided a map with the itinary.<br>"
                f"As an administrator, you can create, store and expose items with a price and category.")

    app.include_router(user_router)
    app.include_router(customer_router)
    app.include_router(deliverydriver_router)
    app.include_router(administrator_router)

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        """Redirect to the API documentation"""
        return RedirectResponse(url="/docs")

    uvicorn.run(app, port=8000, host="0.0.0.0", root_path="/proxy/8000")
