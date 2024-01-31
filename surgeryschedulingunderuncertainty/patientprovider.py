
from abc import ABC, abstractmethod


class PatientProvider(ABC):
    
    def __init__(self, description = ""):
        self.description = ""

    @description.getter
    def description(self):
        return self.description
    
    @description.setter
    def description(self, new_description):
        self.description = new_description
    

    @abstractmethod
    def provide_patient(self, patient_model):
        pass

    @abstractmethod
    def provide_patient_set(self, patient_model, num):
        pass

    @abstractmethod
    def provide_patient_training(self, patient_model, num):
        pass

    
    def provide_sets(self, patient_model, num_patients, num_training):
        return (self.provide_patient_set(patient_model=patient_model, num=num_patients), 
                self.provide_patient_training(patient_model=patient_model, num = num_training))
    


class PatientsFromHistoricalDataProvider(PatientProvider):

    def provide_patient(self, patient_model):
        pass

    def provide_patient_set(self, patient_model, num):
        pass

    def provide_patient_training(self, patient_model, num):
        pass



class PatientsGeneratedProvider(PatientProvider):

    def provide_patient(self, patient_model):
        pass

    def provide_patient_set(self, patient_model, num):
        pass

    def provide_patient_training(self, patient_model, num):
        pass