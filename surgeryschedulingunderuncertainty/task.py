# Python STL

# Packages

# Module's classes
from .master import Master
from .patient import Patient


class Task():

    def __init__(self, 
                 name: str,
                 num_of_weeks: int, 
                 num_of_patients: int,
                 robustness_risk: float,
                 robustness_overtime: int, 
                 patients:list[Patient] = None,
                 master_schedule: Master = None):
        
        self._name = name
        self._num_of_weeks = num_of_weeks
        self._num_of_patients = num_of_patients
        self._robustness_risk = robustness_risk
        self._robustness_overtime = robustness_overtime
        self._patients = patients
        self._master_schedule = master_schedule
        
    # Getters and setters
    def get_name(self):
        return self._name
    
    def set_name(self, new:str):
        self._name = new
    
    name = property(get_name, set_name)

    def get_num_of_weeks(self):
        return self._num_of_weeks
    
    num_of_weeks = property(get_num_of_weeks)

    def get_num_of_patients(self):
        return self._num_of_patients
    
    num_of_patients = property(get_num_of_patients)

    def get_robustness_risk(self):
        return self._robustness_risk
    
    robustness_risk = property(get_robustness_risk)

    def get_robustness_overtime(self):
        return self._robustness_overtime
    
    robustness_overtime = property(get_robustness_overtime)

    def get_patients(self):
        return self._patients
    
    def set_patients(self, new:list[Patient]):
        if len(new) != self._num_of_patients:
            raise ValueError("The length of the list of patients provided does not match the task's number of patients.")
        self._patients = new
    
    patients = property(get_patients, set_patients)

    def get_master_schedule(self):
        return self._master_schedule
    
    def set_master_schedule(self, new:Master):
        self._master_schedule = new
    
    master_schedule = property(get_master_schedule, set_master_schedule)


