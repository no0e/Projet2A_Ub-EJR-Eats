from dotenv import load_dotenv

from src.DAO.AdministratorDAO import AdministratorDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.UserDAO import UserDAO
from src.Service.AdministratorService import AdministratorService
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService

load_dotenv()
db_connector = DBConnector()
user_repo = UserDAO(db_connector)
admin_repo = AdministratorDAO(db_connector)
jwt_service = JwtService()
user_service = UserService(user_repo)
admin_serice = AdministratorService(admin_repo)
