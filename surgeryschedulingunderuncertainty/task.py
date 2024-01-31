




class Task():

    def __init__(self, master_schedule, patients, num_of_weeks, robustness_params, description = ""):
        self.description = description
        self.master_schedule = master_schedule
        self.patients = patients
        self.num_of_weeks = num_of_weeks
        self.robustness_params = robustness_params

    @description.getter
    def description(self):
        return self.description
    
    @description.setter
    def description(self, new_description):
        self.description = new_description


    @master_schedule.getter
    def master_schedule(self):
        return self.master_schedule
    
    @master_schedule.setter
    def master_schedule(self, new_master_schedule):
        self.master_schedule = new_master_schedule


    @patients.getter
    def patients(self):
        return self.patients
    
    @patients.setter
    def patients(self, new_patients):
        self.patients = new_patients


    @num_of_weeks.getter
    def num_of_weeks(self):
        return self.num_of_weeks
    
    @num_of_weeks.setter
    def num_of_weeks(self, new_num_of_weeks):
        self.num_of_weeks = new_num_of_weeks


    @robustness_params.getter
    def robustness_params(self):
        return self.robustness_params
    
    @patients.setter
    def robustness_params(self, new_robustness_params):
        self.robustness_params = new_robustness_params
      





