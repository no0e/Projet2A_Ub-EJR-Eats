from src.App.API import run_app
from src.DAO.DBConnector import DBConnector

if __name__ == "__main__":
    #db_connector = DBConnector()
    #db_connector.execute_sql_file("data/init_db.sql")
    app = run_app()
