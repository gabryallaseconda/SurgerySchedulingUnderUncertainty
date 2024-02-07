# Python STL
from abc import ABC, abstractmethod

# Packages
import ngboost as ngb
import ngboost.distns as ng_dist

# Modules



class PredictiveModel(ABC):
    
    def __init__(self):
        pass

    # Getters and setters

    # Abstract methods

    @abstractmethod
    def train(self, patients):
        pass







class NGBLogNormal(PredictiveModel):

    def __init__(self):
        self.model = ngb.NGBRegressor(Dist = ng_dist.LogNormal, verbose = False)

    @abstractmethod
    def train(self, patients):
        
        #ottenere features e target da patients
        
        self.model.fit(df_x, df_y.duration.ravel() )





class NGBNormal(PredictiveModel):

    def __init__(self):
        pass

    @abstractmethod
    def train(self, patients):
        pass





class XGBQuantile(PredictiveModel):

    def __init__(self):
        pass

    @abstractmethod
    def train(self, patients):
        pass
