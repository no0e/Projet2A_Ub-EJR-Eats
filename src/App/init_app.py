from dotenv import load_dotenv

from src.DAO.AdministratorDAO import AdministratorDAO
from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.DeliveryDriverDAO import DeliveryDriverDAO
from src.DAO.UserDAO import UserDAO
from src.Service.AdministratorService import AdministratorService
from src.Service.CustomerService import CustomerService
from src.Service.DeliveryDriverService import DeliveryDriverService
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService

load_dotenv()
db_connector = DBConnector()
user_repo = UserDAO(db_connector)
admin_repo = AdministratorDAO(db_connector)
driver_repo = DeliveryDriverDAO(db_connector)
customer_repo = CustomerDAO(db_connector)

jwt_service = JwtService()
user_service = UserService(user_repo, admin_repo, driver_repo, customer_repo)
admin_service = AdministratorService(user_repo, admin_repo, driver_repo, customer_repo)
customer_service = CustomerService()
driver_service = DeliveryDriverService()
