# Python STL


# Packages
from pandas import pd

# Modules
from .adversary import ( Equiprobable)
from .master import Master
from .patient import Patient
from .patients_provider import PatientsFromHistoricalDataProvider
from .predictive_model import PredictiveModel
from .task import Task


class Scheduler():
    def __init__(self,
                 name: str,
                 num_of_weeks: int,
                 num_of_patients: int,
                 robustness_risk: float,
                 robustness_overtime: int,
                 num_patients_training: int,

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
        _num_patients_training = num_patients_training

        _master_scheduling = master_scheduling # questo va sistemato

        _patient_provider_type = patient_provider_type
        _predictive_model_type = predictive_model_type
        _uncertainty_model_type = uncertainty_model_type

        _historical_data = historical_data
        _patients_to_be_scheduled = patients_to_be_scheduled
        _patient_generation_profile = patient_generation_profile


    def run(self):

        patient_provider = PatientsFromHistoricalDataProvider(
                        historical_data= historical_data_df
                        )
        
        (_patients, _training_set) = patient_provider.provide_patient_set(quantity = self._num_of_patients, 
                                                                          quantity_training = self._num_patients_training, 
                                                                          equipe_profile = None, 
                                                                          urgency_profile = None)
        
        master = Master()

        _master_scheduling = master.master_creator() #????

        
        predictive_model = Pre
