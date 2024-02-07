# Python STL

# Packages
import numpy as np

# Module's classes
from surgeryschedulingunderuncertainty.uncertainty_profile import UncertaintyProfile

class Patient():

    def __init__(self, id: int, features: np.ndarray, target: float, uncertainty_profile: UncertaintyProfile, equipe: str, urgency: int):
        self._id = id
        self._features = features
        self._target = target
        self._uncertainty_profile = uncertainty_profile
        self._equipe = equipe
        self._urgency = urgency

    # Getters and setters
    def get_id(self):
        return self._id
    
    def set_id(self, new:int):
        self._id = new
    
    id = property(get_id, set_id)

    def get_features(self):
        return self._features
    
    def set_features(self, new:np.ndarray):
        self._features = new
    
    features = property(get_features, set_features)
        
    def get_target(self):
        return self._target
    
    def set_target(self, new:float):
        self._target = new
    
    target = property(get_target, set_target)

    def get_uncertainty_profile(self):
        return self._uncertainty_profile
    
    def set_uncertainty_profile(self, new:UncertaintyProfile):
        self._uncertainty_profile = new
    
    uncertainty_profile = property(get_uncertainty_profile, set_uncertainty_profile)

    def get_equipe(self):
        return self._equipe
    
    def set_equipe(self, new:str):
        self._equipe = new
    
    equipe = property(get_equipe, set_equipe)

    def get_urgency(self):
        return self._urgency
    
    def set_urgency(self, new:int):
        self._urgency = new
    
    urgency = property(get_urgency, set_urgency)
    


