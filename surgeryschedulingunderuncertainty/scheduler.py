# Python STL


# Packages
from pandas import pd

# Modules
from .adversary import ( Equiprobable)
from .patient import Patient
from .task import Task
from .master import Master


class Scheduler():
    def __init__(self,
                 name: str,
                 num_of_weeks: int,
                 num_of_patients: int,
                 robustness_risk: float,
                 robustness_overtime: int,
                 master_scheduling: Master,# no questo va sistemato

                 patient_provider_type:str,
                 predictive_model_type:str,
                 uncertainty_model_type:str,

                 
                 historical_data: pd.DataFrame = None,
                 patients_to_be_scheduled: pd.DataFrame = None,
                 patient_generation_profile: dict = None
                 ):
        
        _name = name
        _num_of_weeks = num_of_weeks
        _num_of_patients = num_of_patients
        _robustness_risk = robustness_risk
        _robustness_overtime = robustness_overtime
        _master_scheduling = master_scheduling # questo va sistemato

        _patient_provider_type = patient_provider_type
        _predictive_model_type = predictive_model_type
        _uncertainty_model_type = uncertainty_model_type

        _historical_data = historical_data
        _patients_to_be_scheduled = patients_to_be_scheduled
        _patient_generation_profile = patient_generation_profile


    def run(self):

        task = Task(name = "My first problem",
            num_of_weeks= 2,
            num_of_patients= 300,
            robustness_risk= 0.2,
            robustness_overtime= 0.9,
            urgency_to_max_waiting_time= {0: 7, 1:30, 2:60, 3:180, 4:360}, 
            )
        
        
        historical_data_df = pd.read_csv("../data/historical_data.csv")

        patient_provider = PatientsFromHistoricalDataProvider(task = task, 
                        historical_data= historical_data_df
                        )
        patient = patient_provider.provide_patient()
        print(patient)
        task.patients = patient_provider.provide_patient_set(quantity=300)
