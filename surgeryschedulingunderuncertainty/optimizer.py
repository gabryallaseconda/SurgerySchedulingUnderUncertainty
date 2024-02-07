# Python STL
from abc import ABC, abstractmethod
import os 

# Packages


# Module's classes
from implementor import Implementor
from adversary import Adversary
from task import Task
from predictive_model import PredictiveModel



class Optimizer(ABC):
    
    def __init__(self, task, description = ""):
        self._tast = task
        self._description = ""

        #self.schedule = None

    # Getters and setters
        
    def get_task(self):
        return self._task
    
    def set_task(self, new:float):
        self._task = new
    
    task = property(get_task, set_task)

    def get_description(self):
        return self._description
    
    def set_description(self, new:float):
        self._description = new
    
    description = property(get_description, set_description)


    @abstractmethod
    def run():
        pass
    


class ImplementorAdversary(Optimizer):

    def __init__(self, task:Task, implementor: Implementor, adversary: Adversary, description = ""):

        super().__init__(task, description)
        
        self._implementor = implementor
        self._adversary = adversary

        self._instance_data = None



    def set_adversary_predictor(self, predictor:PredictiveModel):
        self._adversary.predictor = predictor
        return True


    def run(self, max_loops:int):

        # Main implementor adversary loop
        for loop in range(max_loops):
            flag = False

            # call implementor

            


            # call adversary

            if flag == True:
                break

            # update instance data

        
        #return schedule


    def create_instance_data(self):
        pass

    def run_implementor(self, instance_data):
        # return self.implementor.run(instance_data)
        pass

    def run_adversary(self, schedule):
        # return self.adversary.run(schedule)
        pass

    def update_instance_data(self, adversary_fragilities):
        # update self.instance_data
        pass





