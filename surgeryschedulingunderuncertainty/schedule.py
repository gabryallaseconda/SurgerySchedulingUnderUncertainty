# Python STL
from abc import ABC, abstractmethod
from datetime import datetime

# Packages

# Modules
from .task import Task
from .block import ScheduleBlock


class Schedule(ABC):

    def __init__(self, task:Task, solved_instance):
        
        self._task = task
        self._blocks = []
        self._creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               
        num_of_blocks = task.master_schedule.get_num_of_blocks()
        num_of_patients = task.num_of_patients
        
        
        # First, fill the patients data with the solved instance informations
        for num_pat in range(num_of_patients):
            patient = task.patients[num_pat]
            patient.surgery_day = solved_instance.y[num_pat+1]()
            patient.delay_in_days = solved_instance.z[num_pat+1]()
        
        
        # For each week we have whole set of blocks belonging to the master schedule
        for week in range(task.num_of_weeks):
            
            # We create a new schedule block for every block in master, for every week
            for block_number, master_block in enumerate(task.master_schedule.get_blocks()):
                
                # Calculate the block index
                block_index = week*num_of_blocks + block_number
                
                # Calculate days since the beginning
                days_since_beginning = week*5 + master_block.weekday - 1 # Monday is encoded as 0!
                
                # Instantiate the schedule block getting the infos from the master block
                block = ScheduleBlock(
                    duration= master_block.duration, 
                    equipes= master_block.equipes, 
                    room = master_block.room,
                    weekday= master_block.weekday, 
                    week = week,
                    days_since_beginning=days_since_beginning,
                    order_in_day= master_block.order_in_day, 
                    order_in_week= week,  # convention 0s and 1s in python
                    order_in_schedule=block_index, # on models is block_index+1 
                )
                
                # We have to look through all the patients indexes                
                for num_pat in range(num_of_patients):
                    
                    # Check if the solution assign the patient to the block
                    #epsilon = 0.05  # not perfectly 1!!!
                    #if abs(solved_instance.x[block_index+1, num_pat+1]() - 1) < epsilon:
                        
                    if solved_instance.x[block_index+1, num_pat+1]() > 0.8:
                        
                        # Get the patient indexing the patients list in task
                        patient = task.patients[num_pat]
                        
                        #patient.surgery_day = solved_instance.y[num_pat+1]()
                        #patient.delay_in_days = solved_instance.z[num_pat+1]()
                        
                        # Add the patient to the current block
                        block.add_patient(patient)
                        
                self._blocks.append(block)
                
    def export_schedule(self):
        data_dictionary = {
            'task description': self._task.name,
            'creation date': self._creation_date,
            'number of blocks': len(self._blocks),
            'blocks':[],
            'patients_not_included':[]
        }
        
        for block in self._blocks:
            data_dictionary['blocks'].append(block.retrieve_insights())
            
        # Get the list of patients included in the schedule
        patients_included = []
        # Loop on the blocks
        for block in self._blocks:
            patients_in_block = block.patients
            # Loop inside each block
            for patient in patients_in_block:
                patients_included.append(patient.id)
         
        # # Get the list of non included patients, and other metrics
        # patients_not_included = []
        # patients_not_included_urgency = []
        # patients_not_included_days_diff = []
        # patients_not_included_equipe = []
        # patients_not_included_duration_nominal = []
        # # Loop on patients in the task
        # for patient in self._task.patients:
        #     if patient.id not in patients_included:
        #         patients_not_included.append(patient.id)
        #         patients_not_included_urgency.append(patient.urgency)
        #         patients_not_included_days_diff.append(patient.max_waiting_days - patient.days_waiting)
        #         patients_not_included_equipe.append(patient.equipe)
        #         patients_not_included_duration_nominal.append(patient.uncertainty_profile.nominal_value)
        
        # data_dictionary.update({
        #     'patients not included' : patients_not_included,
        #     'patients not included urgency' : patients_not_included_urgency,
        #     'patients not included days difference' : patients_not_included_days_diff,
        #     'patients not included equipe' : patients_not_included_equipe,
        #     'patients not included duration nominal' : patients_not_included_duration_nominal
        # })
        
        
        # Extract information of patients not included
        patients_not_included = []
        
        for patient in self._task.patients:
            if patient.id not in patients_included:
                pat_data = {'id': patient.id,
                            'urgency': patient.urgency,
                            'days difference': patient.max_waiting_days - patient.days_waiting,
                            'equipe': patient.equipe,
                            'duration nominal': patient.uncertainty_profile.nominal_value,
                            'uncertainty parameters': patient.uncertainty_profile.uncertainty_summary(),
                            'surgery_day':patient.surgery_day,
                            'delay_in_days':patient.delay_in_days}
                data_dictionary['patients_not_included'].append(pat_data)
        
        
            
        return data_dictionary
    
    def write_schedule_insights(self):
        pass
                    
                    
                    
                
        
    
        
        
        




    # Getters and setters