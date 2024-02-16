# Python STL
from abc import ABC, abstractmethod

# Packages
import numpy as np
import ngboost as ngb
import ngboost.distns as ng_dist

# Modules
from patient import Patient
from uncertainty_profile import UncertaintyProfile


class PredictiveModel(ABC):
    """
    Abstract class for predictive model. Models trained with these classes are 
    probabilistic regressor which returns prediction on surgery duration according
    the characteristics of the patients and the surgeries. The resulting prediction
    are returned in the format of uncertainty profile.
    

    Attributes
    ----------
    _patients : list[Patient]
        The list of patients that will be used as to train the model.
    _description : str
        To keep a text description of the model created.

    Methods
    -------
    train(self, patients:list[Patient]) -> None:
        Abstract method, create a model and train it on the given patients.
    predict_form_patients(self, inference_patients: list[Patient]) -> UncertaintyProfile:
        Abstract method, given a list of patients, this run the trained model to produce prediction
        in the format of uncertainty profile.
    extract_training_data(self)
    """
    
    def __init__(self, patients: list[Patient], description = ""):
        self._patients = patients
        self._description = description

        self._training_features, self._training_target = self.extract_training_data()

    # Getters and setters 
               
    def get_description(self):
        return self._description
    
    def set_description(self, new:str):
        self._description = new
    
    description = property(get_description, set_description)

    # Abstract methods

    @abstractmethod
    def train(self, patients):
        pass

    @abstractmethod
    def predict_from_patients(self, inference_patients: list[Patient]):
        pass


    # General methods 
    def extract_training_data(self):

        features_list = []
        target_list = []

        for patient in self.patients:
            features_list.append(patient.features)
            target_list.append(patient.target)

        return (np.vstack(features_list), np.vstack(target_list))
    
    def extract_features(self, inference_patients: list[Patient]):

        features_list = []

        for patient in inference_patients:
            features_list.append(patient.features)

        return np.vstack(features_list)









class NGBLogNormal(PredictiveModel):

    def __init__(self):
        super().__init__(task, description)
        self.model = ngb.NGBRegressor(Dist = ng_dist.LogNormal, verbose = False)

    def train(self, patients):
                
        self.model.fit(self.training_features, self.training_target.ravel() )







class NGBNormal(PredictiveModel):

    def __init__(self):
        pass

    def train(self, patients):
        pass





class XGBQuantile(PredictiveModel):

    def __init__(self):
        pass

    @abstractmethod
    def train(self, patients):
        pass
