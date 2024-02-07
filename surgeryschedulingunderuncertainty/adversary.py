# Python STL
from abc import ABC, abstractmethod

# Packages

# Module's classes
from predictive_model import PredictiveModel
from schedule import Schedule


class Adversary(ABC): 

    def __init__(self, predictor:PredictiveModel, schedule:Schedule, description = ""):
        self._description = description
        self._predictor = predictor
        self._schedule = schedule
        
    # Getters and setter
    def get_description(self):
        return self._description
    
    def set_description(self, new:str):
        self._description = new
    
    description = property(get_description, set_description)

    def get_predictor(self):
        return self._predictor
    
    def set_predictor(self, new:PredictiveModel):
        self._predictor = new
    
    predictor = property(get_predictor, set_predictor)

    def get_schedule(self):
        return self._schedule
    
    def set_schedule(self, new:Schedule):
        self._schedule = new
    
    schedule = property(get_schedule, set_schedule)

    # Abstract methods
    @abstractmethod
    def run(self):
        pass


class Equiprobable(Adversary):

    def __init__(self, predictor:PredictiveModel, schedule:Schedule, description = ""):
        super().__init__(predictor, schedule, description)
    
