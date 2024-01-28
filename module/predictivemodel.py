from abc import ABC, abstractmethod


class PredictiveModel(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def train(self, patients):
        pass







class NGBLogNormal(PredictiveModel):

    def __init__(self):
        pass

    @abstractmethod
    def train(self, patients):
        pass







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
