# Python STL
from abc import ABC, abstractmethod

# Packages
import numpy as np
import ngboost as ngb
import ngboost.distns as ng_dist

# Modules
from .patient import Patient
from .uncertainty_profile import (
    UncertaintyProfile, 
    LogNormalDistribution,
    NormalDistribution
)


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
    _training_features: np.ndarray
        A list containing the features for each patient to be used for training.
    _training_target: np.ndarray
        A list containing the target for each patient to be used for training.

    Methods
    -------
    predict_form_patients(self, inference_patients: list[Patient]) -> list[Patient]:
        Abstract method, given a list of patients, this run the trained model to update that list
        with patients having uncertainty profile filled according to the model.
    _extract_training_data(self) -> tuple[np.ndarray]
        Method to extract features and target from each patient.
    _extract_features(self, inference_patients: list[Patient]) -> np.ndarray
        Method to extract features from a list of patients in order to get probabilistic predicitons
        on their surgery duration. Used in inference phase.
    """
    
    def __init__(self, patients: list[Patient], description = ""):
        self._patients = patients
        self._description = description

        self._training_features, self._training_target = self._extract_training_data()
        self._trained = False

    # Getters and setters 
               
    def get_description(self):
        return self._description
    
    def set_description(self, new:str):
        self._description = new
    
    description = property(get_description, set_description)

    # Abstract methods

    @abstractmethod
    def predict(self, inference_patients: list[Patient]):
        """
        Provide a single patient. Can request an equipe and/or an urgency.

        Parameters
        ----------
        inference_patients: list[Patient]
            A list of patients for which the surgery prediction will be predicted.
            "Features" of each Patient will be used.

        Returns
        -------
        patients
            The updated list of patients, this is the same list as inference_patients
            but whith the member uncertainty_profile filled according to the model.
        """
        pass


    # General methods 
    def _extract_training_data(self):

        features_list = []
        target_list = []

        for patient in self._patients:
            features_list.append(patient.features)
            target_list.append(patient.target)

        return (np.vstack(features_list), np.vstack(target_list))
    

    def _extract_features(self, inference_patients: list[Patient]) -> np.ndarray:
        """Questa funzione potrebbe essere completamente inutile.

        Args:
            inference_patients (list[Patient]): _description_

        Returns:
            np.ndarray: _description_
        """

        features_list = []

        for patient in inference_patients:
            features_list.append(patient.features)

        return np.vstack(features_list)



class NGBLogNormal(PredictiveModel):
    """
    Inherit from abstract class Predictive model.
    This class wraps NG Boost model Log Normal distribution. Must be trained in 
    order to be 
    
    Attributes
    ----------
    _patients : list[Patient]
        The list of patients that will be used as to train the model.
    _description : str
        To keep a text description of the model created.

    Methods
    -------
    provide_patient(self, requested_equipe:str = None, requested_urgency:int = None) -> Patient:
        Provide a single patient, can specify equpe and urgency
    """

    def __init__(self, patients: list[Patient], description = ""):
        super().__init__(patients = patients, description = description)
        
        # Instantiate the model and train
        self._model = ngb \
            .NGBRegressor(Dist = ng_dist.LogNormal, verbose = False) \
            .fit(self._training_features, self._training_target.ravel() ) 


    def train(self):
        self._model.fit(self._training_features, self._training_target.ravel() )

    def predict(self, inference_patients: list[Patient]):
        """
        Provide a single patient. Can request an equipe and/or an urgency.

        Parameters
        ----------
        inference_patients: list[Patient]
            A list of patients for which the surgery prediction will be predicted.
            "Features" of each Patient will be used.

        Returns
        -------
        patients
            The updated list of patients, this is the same list as inference_patients
            but whith the member uncertainty_profile filled according to the model.
        """

        # Get the list of the features (an element for each patient in the list)
        features = self._extract_features(inference_patients=inference_patients)

        # Run the model
        predictions = self._model.pred_dist(features).params

        # Initalize a new empty list of patients
        patients = []

        # Cicle on initial list inference_patients
        for ind, patient in enumerate(inference_patients):
            # Get patient parameter
            param_s = predictions.get('s')[ind]
            param_scale = predictions.get('scale')[ind]

            # Update patient by creating uncertanty profile object
            patient.uncertainty_profile = LogNormalDistribution(param_s=param_s, param_scale=param_scale)
            
            patients.append(patient)

        return patients
        









class NGBNormal(PredictiveModel):
    """
    Inherit from abstract class Predictive model.
    This class wraps NG Boost model Log Normal distribution. Must be trained in 
    order to be 
    
    Attributes
    ----------
    _patients : list[Patient]
        The list of patients that will be used as to train the model.
    _description : str
        To keep a text description of the model created.

    Methods
    -------
    provide_patient(self, requested_equipe:str = None, requested_urgency:int = None) -> Patient:
        Provide a single patient, can specify equpe and urgency
    """

    def __init__(self, patients: list[Patient], description = ""):
        super().__init__(patients = patients, description = description)
        
        # Instantiate the model and train
        self._model = ngb \
            .NGBRegressor(Dist = ng_dist.Normal, verbose = False) \
            .fit(self._training_features, self._training_target.ravel() ) 


    def train(self):
        self._model.fit(self._training_features, self._training_target.ravel() )

    def predict(self, inference_patients: list[Patient]):
        """
        Provide a single patient. Can request an equipe and/or an urgency.

        Parameters
        ----------
        inference_patients: list[Patient]
            A list of patients for which the surgery prediction will be predicted.
            "Features" of each Patient will be used.

        Returns
        -------
        patients
            The updated list of patients, this is the same list as inference_patients
            but whith the member uncertainty_profile filled according to the model.
        """

        # Get the list of the features (an element for each patient in the list)
        features = self._extract_features(inference_patients=inference_patients)

        # Run the model
        predictions = self._model.pred_dist(features).params

        # Initalize a new empty list of patients
        patients = []

        # Cicle on initial list inference_patients
        for ind, patient in enumerate(inference_patients):
            # Get patient parameter
            param_loc = predictions.get('loc')[ind]
            param_scale = predictions.get('scale')[ind]

            # Update patient by creating uncertanty profile object
            patient.uncertainty_profile = NormalDistribution(param_loc=param_loc, param_scale=param_scale)
            
            patients.append(patient)

        return patients
        





class XGBQuantile(PredictiveModel):

    def __init__(self):
        pass

    @abstractmethod
    def train(self, patients):
        pass
