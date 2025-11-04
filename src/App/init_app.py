from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector
from src.DAO.UserDAO import UserDAO
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService

load_dotenv()
db_connector = DBConnector()
user_repo = UserDAO(db_connector)
jwt_service = JwtService()
user_service = UserService(user_repo)
