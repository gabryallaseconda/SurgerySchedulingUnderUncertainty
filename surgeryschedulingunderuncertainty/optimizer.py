
from dotenv import load_dotenv
load_dotenv()
import os 

# ABstract Classes
from abc import ABC, abstractmethod

# Package for mathematical programming modelling



class Optimizer(ABC):
    
    def __init__(self, task, description = ""):
        self.tast = task
        self.description = ""

        self.schedule = None


    @task.getter
    def task(self):
        return self.task
    
    @task.setter
    def task(self, new_task):
        self.task = new_task

    
    @description.getter
    def description(self):
        return self.description
    
    @description.setter
    def description(self, new_description):
        self.description = new_description
    

    @abstractmethod
    def run():
        pass
    


####################
#### Optimizer: implementor adversary

class ImplementorAdversary(PatientProvider):

    def __init__(self, task, implementor, adversary, description = ""):

        super().__init__(task, description)
        
        self.implementor = implementor
        self.adversary = adversary

        self.instance_data = None



    def set_adversary_predictor(self, predictor):
        self.adversary.predictor = predictor
        return True


    def run(self, max_loops = 0):
        # Setting the number of max loops. If not setted then load it from environment variable.
        if max_loops == 0:
            max_loops = os.environ.get("MAXIMUM_IMPLEMENTOR_ADVERSARY_LOOPS")

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





def Adversary(ABC): # da completare
    def __init__(self, predictor, schedule, description = ""):
        self.predictor = predictor
        self.schedule = schedule
        self.description = description
        

    @schedule.getter
    def schedule(self):
        return self.schedule
    
    @schedule.setter
    def schedule(self, new_schedule):
        self.schedule = new_schedule
    

    @instance_data.getter
    def instance_data(self):
        return self.instance_data
    
    @instance_data.setter
    def instance_data(self, new_instance_data):
        self.instance_data = new_instance_data


    @abstractmethod
    def run(self):
        pass
    