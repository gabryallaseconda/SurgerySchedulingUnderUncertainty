# Python STL
from abc import ABC, abstractmethod
import random

# Packages
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# Modules
from .patient import Patient


class PatientsProvider(ABC):
    """
    Abstract class for patients providers. Patients providers are object which
    generates patient. They can process dataset and extract a patient for each line
    or they can generate patients with random process. These different ways are
    implemented in different concrete classes. Generation can be driven by asking 
    for specific kind of patients, in particular specifing the equipe or the 
    urgency. Patients providers also can generate patients for the training of 
    predictive models.

    Attributes
    ----------
    _description : str
        To keep a text description of the provider created.

    Methods
    -------
    provide_patient(self, requested_equipe:str = None, requested_urgency:int = None) -> Patient:
        Provide a single patient, can specify equpe and urgency
    """

    
    def __init__(self, description = ""):
        self._description = description

    # Getters and setters
    def get_description(self):
        return self._description
    
    def set_description(self, new:str):
        self._description = new
    
    description = property(get_description, set_description)


    # Abstract methods
    @abstractmethod
    def provide_patient(self, requested_equipe:str = None, requested_urgency:int = None) -> Patient:
        pass

    @abstractmethod
    def provide_patients(self, 
                         quantity: int, 
                         equipe_profile:dict = None, 
                         urgency_profile:dict = None, 
                         include_target: bool = True) -> list[Patient]:
        pass

    @abstractmethod
    def provide_patient_set(self, 
                            quantity: int, 
                            equipe_profile:dict = None, 
                            urgency_profile:dict = None) -> list[Patient]:
        pass

    @abstractmethod
    def provide_patient_training(self, 
                                 quantity: int, 
                                 equipe_profile:dict = None, 
                                 urgency_profile:dict = None) -> list[Patient]:
        pass

    # General methods
    def provide_sets(self, quantity, quantity_training, equipe_profile, urgency_profile):
        return (self.provide_patient_set(quantity=quantity, equipe_profile=equipe_profile, urgency_profile=urgency_profile), 
                self.provide_patient_training(quantity=quantity_training, equipe_profile=equipe_profile, urgency_profile=urgency_profile))
    


class PatientsFromHistoricalDataProvider(PatientsProvider):
    """
    Inherit from abstract class PatientsProvider
    Class for a patients provider that extract patients from a dataset of already
    processed patients. In general this kind of patients can be used for test purposes
    or to train the predictive models. The Dataset must contain some columns with the 
    following names:
     - target (float): the true surgery time.
     - equipe (str): which equipe have processed the patient.
     - urgency (int): urgency grade required. Urgency grades are converted as 
       specified in the task object.
     - other columns: will be treated as "features" for predicting the surgery time.
       Numerical columns are preserved, categorical are encoded through one-hot-encoding.
    
    Attributes
    ----------
    _description: str
        To keep a text description of the provider created.
    _historical_data: pd.DataFrame
        Is the pandas' dataframe which provide patients' data.
    _sampled_indexes: set
        Keep track of rows already used from the dataset.
    _patient_id_start_number: int
        When all rows are used, the function restart sampling including already used rows.
        This variable allow to generate patients with different ids. 

    Methods
    -------
    provide_patient(self, requested_equipe:str = None, requested_urgency:int = None) -> Patient:
        Provide a single patient, can specify equpe and urgency
    """

    def __init__(self, 
                 historical_data: pd.DataFrame, 
                 description = ""):
        """
        Constructor.

        Parameters
        ----------
        _description : str, optional
            To keep a text description of the provider created.
        _historical_data: pd.DataFrame
            Is the pandas' dataframe which provide patients' data.
        """
        super().__init__(task, description)
        
        self._historical_data = historical_data
        
        self._sampled_indexes = set()
        self._patient_id_start_number = 0

        ## One hot encoding of categorical features

        # Select columns containing categorical data  (object type)
        categorical_columns = self._historical_data.select_dtypes(include=['object']).columns
        # Instantiate one - hot- tencoder
        encoder = OneHotEncoder( drop='first')
        # Run the one - hot - encoder
        one_hot_encoded = encoder.fit_transform(self._historical_data[categorical_columns])
        # New dataframe
        one_hot_encoded_df = pd.DataFrame(one_hot_encoded.toarray(), columns=encoder.get_feature_names_out(categorical_columns))
        # Concatenatign with original dataframe
        df = pd.concat([self._historical_data, one_hot_encoded_df], axis=1)
        # Exclude equipe columns
        categorical_columns = categorical_columns.difference(['equipe'])
        # Removing encoded columns
        self._historical_data = df.drop(columns=categorical_columns)


    # Getters and setters
    def get_historical_data(self):
        return self._historical_data
    
    def set_historical_data(self, new:pd.DataFrame):
        self._historical_data = new
    
    historical_data = property(get_historical_data, set_historical_data)


    # Abstract methods implementation

    def provide_patient(self, requested_equipe:str = None, requested_urgency:int = None, include_target: bool = True) -> Patient:

        """
        Provide a single patient. Can request an equipe and/or an urgency.

        Parameters
        ----------
        requested_equipe: str, optional
            The equipe which will process the patient provided.

        requested_urgency: int, optional
            The urgency grade assigned to the patient.

        Returns
        -------
        Patient
            A patient object filled with information in the dataset.
        """

        if (requested_equipe != None) & (requested_equipe != None):
            filtered_data = self._historical_data.loc[
                (self._historical_data['equipe'] == requested_equipe) &
                (self._historical_data['urgency'] == requested_urgency)
            ]
        elif requested_equipe != None:
            filtered_data = self._historical_data.loc[
                (self._historical_data['equipe'] == requested_equipe)
            ]
        elif requested_urgency != None:
            filtered_data = self._historical_data.loc[
                (self._historical_data['urgency'] == requested_urgency)
            ]
        else: filtered_data = self._historical_data

        available_indexes = [ x for x in list(filtered_data.index) if x not in self._sampled_indexes]
        patient_index = random.choice(available_indexes)
        self._sampled_indexes.add(patient_index)

        id = patient_index + self._patient_id_start_number
        features = np.array(self._historical_data.loc[patient_index, ~self._historical_data.columns.isin(['equipe', 'target', 'urgency'])])
        
        if include_target:
            target = self._historical_data.loc[patient_index, 'target']
        else:
            target = None
        
        equipe = self._historical_data.loc[patient_index, 'equipe']
        urgency = self._historical_data.loc[patient_index, 'urgency']

        return Patient(id=id,equipe=equipe, urgency=urgency, features=features, target=target, uncertainty_profile=None)
    

    def provide_patients(self, 
                         quantity: int, 
                         equipe_profile:dict = None, 
                         urgency_profile:dict = None, 
                         include_target: bool = True) -> list[Patient]:
        
        tollerance = 1e-6

        if equipe_profile:
            equipes = np.array(list(equipe_profile.keys()))
            equipes_prob = np.array(list(equipe_profile.values()))
            
            if not np.isclose(sum(equipes_prob), 1.0, atol=tollerance):
                raise ValueError(f"The sum of probabilities for equipe is not one (tolerance={tollerance}).")

        if urgency_profile:
            urgencies = np.array(list(urgency_profile.keys()))
            urgencies_prob = np.array(list(urgency_profile.keys()))
            
            if not np.isclose(sum(urgencies_prob), 1.0, atol=tollerance):
                raise ValueError(f"The sum of probabilities for urgency is not one (tolerance={tollerance}).")
            
        patient_list = []    

        for i in range(quantity):
            if equipe_profile:
                equipe = np.random.choice(equipes, p=equipes_prob)
            else:
                equipe = None

            if urgency_profile:
                urgency = np.random.choice(urgencies, p=urgencies_prob)
            else:
                urgency = None

            patient_list.append(self.provide_patient(requested_equipe = equipe, 
                                       requested_urgency = urgency, 
                                       include_target = include_target))
            
        return patient_list


    def provide_patient_set(self, 
                            quantity: int, 
                            equipe_profile:dict = None, 
                            urgency_profile:dict = None) -> list[Patient]:
        
        return self.provide_patients(quantity = quantity, 
                                     equipe_profile = equipe_profile, 
                                     urgency_profile = urgency_profile, 
                                     include_target = False)
        

    def provide_patient_training(self, 
                            quantity: int, 
                            equipe_profile:dict = None, 
                            urgency_profile:dict = None) -> list[Patient]:
        
        return self.provide_patients(quantity = quantity, 
                                     equipe_profile = equipe_profile, 
                                     urgency_profile = urgency_profile, 
                                     include_target = True)

    # Specific methods

    def reset_sampled_indexes(self, enforce = False):
        """_summary_
        Quando chiamata, se forzata o se tutti i pazienti sono stati estratti, si resetta il contenitore
        degli indici già estratti.
        Args:
            enforce (bool, optional): _description_. Defaults to False.
        """
        if enforce | (len(self._historical_data.index) == self._sampled_indexes):
            print("Warning: from now on patients can be resampled.")
            self._sampled_indexes = set()
            self._patient_id_start_number += len(self._historical_data) # aggiungo righe su id



class PatientsGeneratedProvider(PatientsProvider):

    # Abstract methods implementation

    def provide_patient(self, patient_model):
        pass

    def provide_patient_set(self, patient_model, num):
        pass

    def provide_patient_training(self, patient_model, num):
        pass