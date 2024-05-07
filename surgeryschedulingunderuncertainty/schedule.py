# Python STL
from abc import ABC, abstractmethod

# Packages

# Modules
from .task import Task
from .block import ScheduleBlock


class Schedule(ABC):

    def __init__(self, task:Task, solved_instance):
        
        self._blocks = []
        
        num_of_blocks = task.master_schedule.get_num_of_blocks()
        num_of_patients = task.num_of_patients
        
        # For each week we have whole set of blocks belonging to the master schedule
        for week in range(task.num_of_weeks):
            
            # We create a new schedule block for every block in master, for every week
            for block_number, master_block in enumerate(task.master_schedule.get_blocks()):
                
                # Calculate the block index
                block_index = week*num_of_blocks + block_number
                
                # Instantiate the schedule block getting the infos from the master block
                block = ScheduleBlock(
                    duration= master_block.duration, 
                    equipes= master_block.equipes, 
                    room = master_block.room,
                    weekday= master_block.weekday, 
                    order_in_day= master_block.order_in_day, 
                    order_in_week= week,  # convention 0s and 1s in python
                    order_in_schedule=block_index, # on models is block_index+1 
                )
                
                # We have to look through all the patients indexes                
                for num_pat in range(num_of_patients):
                    
                    # Check if the solution assign the patient to the block
                    if solved_instance.x[block_index+1, num_pat+1]() == 1:
                        
                        # Get the patient indexing the patients list in task
                        patient = task.patients[num_pat]
                        # Add the patient to the current block
                        block.add_patient(patient)
                        
                self._blocks.append(block)
                    
                    
                    
                
        
    
        
        
        




    # Getters and setters