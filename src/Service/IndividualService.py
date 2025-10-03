from src.Model.Individual import Individual


class IndividualService():
    individual_db: None

    def __init__(self, individual_db: None):
        self.individual_db = individual_db

    
