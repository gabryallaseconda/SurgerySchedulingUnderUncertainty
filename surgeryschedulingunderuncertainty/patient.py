

from surgeryschedulingunderuncertainty.uncertainty_profile import UncertaintyProfile

class Patient():

    def __init__(self, id, features, target, uncertainty_profile:UncertaintyProfile, equipe, urgency):
        self.id = id
        self.features = features
        self.target = target
        self.uncertainty_profile = uncertainty_profile
        self.equipe = equipe
        self.urgency = urgency

    # getters and setter
        

    


