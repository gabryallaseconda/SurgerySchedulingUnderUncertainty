# Python STL

# Packages

# Modules
from .master import Master
from .patient import Patient


class Task():
    """
    Data class to represent the problem. It contains the name of the task as well
    many problem parameters like the number of weeks and the robustness parameters.
    Moreover, these object can be completed after the initialization by providing 
    the list of patients to be scheduled and the master scheduling.
    This class handle the profile urgency that belongs to the problem. By setting
    the relation between urgency and the maximum waiting time allowed it deduce
    the relation between urgency and urgency grade.

        Attributes
    ----------
    _name: str
        Name of the task or the problem.
    _num_of_weeks: int
        How many times the master schedule is repeaded in the final schedule.
    _num_of_patients: int
        Number of the patients that have to be scheduled. Note that not all the 
        patients may be included in the solved schedule.
    _robustness_risk: float
        Robustness parameter describing the probability allowed of having overtime.
        # TODO: revisionare questo
    _robustness_overtime: int
        Robustness parameter describing the allowed overtime in minutes. # TODO anche questo
    _urgency_to_max_waiting_days: dict
        A dictionary mapping the urgency parameter to the max waiting time in days
        allowed for a patient.
    _urgency_to_urgency_grades: dict
        A dictionary mapping the urgency parameter to the urgency grade, that can 
        be used in objective functions to give different priorities to patients.
    _patients: list[Patient], optional
        The list of patients to be scheduled. It's a list of objects of Patient 
        type. This can be provided after instantiation.
    _master_schedule: Master, optional
        The master scheduling. This can be provided after instatiation.

    """

    def __init__(self, 
                 name: str,
                 num_of_weeks: int, 
                 num_of_patients: int,
                 robustness_risk: float,
                 robustness_overtime: int,
                 urgency_to_max_waiting_days: dict = None, 
                 patients:list[Patient] = None,
                 master_schedule: Master = None,
                 gamma_max:int = 10,
                 ):
        
        self._name = name
        self._num_of_weeks = num_of_weeks
        self._num_of_patients = num_of_patients
        self._robustness_risk = robustness_risk
        self._robustness_overtime = robustness_overtime
        self._urgency_to_max_waiting_days = urgency_to_max_waiting_days # optional argument!
        
        self._num_adversary_realizations = 0
        
        self._gamma_max = gamma_max
        
        
        
        #if patients & master_schedule:
            
        
        self._patients = patients # Attenzione che qui vanno verificate le equipes
        self._master_schedule = master_schedule # Attenzione che qui vanno verificate le equipes
        
        
        ## From urgency to max waiting time getting mapping for urgency grades

        # Get original keys and sorted
        ordered_keys = sorted(self._urgency_to_max_waiting_days.keys())
        # Getting respective values
        values = [self._urgency_to_max_waiting_days[key] for key in ordered_keys]
        # Inverting the value list
        inverted_values = values[::-1]
        # Creating the new mapping dictionary
        self._urgency_to_urgency_grades = dict(zip(ordered_keys, inverted_values))


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
    def set_robustness_risk(self, new:float):
        self._robustness_risk = new
    
    robustness_risk = property(get_robustness_risk, set_robustness_risk)

    def get_robustness_overtime(self):
        return self._robustness_overtime
    def set_robustness_overtime(self, new:float):
        self._robustness_overtime = new
    
    robustness_overtime = property(get_robustness_overtime, set_robustness_overtime)


    def get_urgency_to_max_waiting_days(self):
        return self._urgency_to_max_waiting_days
    
    urgency_to_max_waiting_days = property(get_urgency_to_max_waiting_days)


    def get_urgency_to_urgency_grades(self):
        return self._urgency_to_urgency_grades
    
    urgency_to_urgency_grades = property(get_urgency_to_urgency_grades)


    def get_patients(self):
        return self._patients
    
    def set_patients(self, new:list[Patient]):
        """
        Some checks are performed:  that the length of the provided list matches the 
        num_of_patients member, that there are not two or more patients with the same
        id.
        """

        # TODO bisogna verificare che le equipe combacino con quelle del master schedule
        

        if len(new) != self._num_of_patients:
            raise ValueError("The length of the list of patients provided does not match the task's number of patients.")
        
        patient_ids = [x.id for x in new]
        if len(patient_ids) != len(set(patient_ids)):
            raise ValueError("In the given list, there are patients with the same id.")
        
        
        # Apply urgency_to_max_waiting_days
        
        if self._urgency_to_max_waiting_days:
            for patient in new:
                patient.max_waiting_days = self._urgency_to_max_waiting_days.get(patient.urgency)
        
        self._patients = new
    
    patients = property(get_patients, set_patients)

    def get_master_schedule(self):
        return self._master_schedule
    
    def set_master_schedule(self, new:Master):
        self._master_schedule = new
        # TODO: qui bisogna verificare il formato
        # e che le equipe combacino con i pazienti
    
    master_schedule = property(get_master_schedule, set_master_schedule)
    
    
    def get_gamma_max(self):
        return self._gamma_max
    def set_gamma_max(self, new:int):
        self._gamma_max = new
    gamma_max = property(get_gamma_max, set_gamma_max)
    
    
    def get_num_adversary_realizations(self):
        return self._num_adversary_realizations
    num_adversary_realizations = property(get_num_adversary_realizations)


    def add_adversary_realization(self, adversary_realization: dict):        
        patients_ids = adversary_realization.keys()
        
        # Loop on the patients inside the task
        for patient in self.patients:
            # Check if the patient is inside the realization
            if patient.id in patients_ids:
                # If it is, assign the realization as the value suggested by the adversary
                patient.add_adversary_realization(adversary_realization.get(patient.id))
            else:
                # If not, assign zero as a realization
                patient.add_adversary_realization(0.0) 
            
        self._num_adversary_realizations += 1
        

        

