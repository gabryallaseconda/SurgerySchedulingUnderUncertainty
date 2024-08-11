# Python STL
from abc import ABC, abstractmethod

# Packages
#import pyomo.environ as pyo  # not used for the implementor adversary
import numpy as np
import scipy.stats as ss
import numpy as np


# Modules
from .implementor import Implementor, ChanceConstraintsImplementor
from .adversary import Adversary, EquiprobableVertex
from .task import Task
from .predictive_model import PredictiveModel
from .schedule import Schedule
from .report import ReportForImplementorAdversary, ReportForDirectOptimization



class Optimizer(ABC):
    
    def __init__(self, task, description = ""):
        self._task = task
        self._description = description

        #self.schedule = None

    # Getters and setters
    def get_task(self):
        return self._task
    def set_task(self, new:float):
        self._task = new
    task = property(get_task, set_task)

    def get_description(self):
        return self._description
    
    def set_description(self, new:float):
        self._description = new
    
    description = property(get_description, set_description)

    # Abstract methods
    @abstractmethod
    def run():
        pass
    


class ImplementorAdversary(Optimizer):

    def __init__(self, task:Task, implementor: Implementor, adversary: Adversary, description = ""):

        super().__init__(task, description)
        
        self._implementor = implementor
        self._adversary = adversary

        self._instance_data = None
        
        self._report = ReportForImplementorAdversary(task=task, description=description)

    # Getters and setters

    #def set_adversary_predictor(self, predictor:PredictiveModel):
    #    self._adversary.predictor = predictor
    #    return True

    # Abstract methods implementation
    def run(self, max_loops:int):
        
        self._report.start_reporting()
        self._report.start_iterations_reporting()
        
        # Main implementor adversary loop
        for _ in range(max_loops):
            
            # Creating instance
            self.create_instance()
            
            # Call implementor
            print('implementor')
            solved_instance = self._implementor.run()
            schedule =  Schedule(task = self.task, solved_instance = solved_instance)
            
            # Call adversary
            print('adversary')
            adversary = EquiprobableVertex(schedule=schedule, task = self.task)
            robustness_flag, fragile_blocks = adversary.run()
            
            # Save iteration duration and flag
            self._report.report_iteration(flag = robustness_flag)
        
            # Exit the loop if the schedule is robust and do not need other iterations
            if robustness_flag:
                break
            
            
            
        self._report.end_reporting()
        return schedule.export_schedule(), self._report.export_report() #, solved_instance

    # Specific methods
    def create_instance(self):
        
        master_schedule = self._task.get_master_schedule()
        
        # Parameters for sets
        n_days = self._task.num_of_weeks * master_schedule.get_week_length()
        
        #n_week_days = master_schedule.get_week_length
        n_rooms = master_schedule.get_num_of_rooms()
                    
        c_exclusion = 1  #TODO
        c_delay = 1  #TODO
        
        # Get patients
        patients = self._task.get_patients()
        n_pats = self._task.num_of_patients
        
        # Get master blocks
        master_blocks = master_schedule.get_blocks()
        n_master_blocks = master_schedule.get_num_of_blocks()
        n_schedule_blocks = master_schedule.get_num_of_blocks() * self._task.num_of_weeks 

        # Instance data structure initialization
        instance = {}

        # Parameter g (gamma - capacity)
        update_dictionary = {}

        for b in range(n_schedule_blocks):
            
            master_block_index = b % n_master_blocks

            update_dictionary.update \
                    ({(b + 1): master_blocks[master_block_index].duration })
                
        instance.update({'g': update_dictionary})
        
        # Parameter a (compatibility)

        update_dictionary = {}
        
        for b in range(n_schedule_blocks):
            
            master_block_index = b % n_master_blocks
            
            for i, patient in enumerate(patients):

                patient_equipe = patient.equipe
                block_equipes = master_blocks[master_block_index].equipes
                
                if patient_equipe in block_equipes:
                    update_dictionary.update({(b+1,i+1) : 1})
                else:
                    update_dictionary.update({(b+1,i+1) : 0})

        instance.update({'a': update_dictionary})
        
        # TODO il ciclo sui pazieti potrebbe diventare unico...

        # Parameter t (estimated surgery duration time)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.uncertainty_profile.nominal_value})

        instance.update({'t': update_dictionary})

        # Parameter u (Urgency)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.urgency})

        instance.update({'u': update_dictionary})

        # Parameter w (Waiting days already spent)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.days_waiting})

        instance.update({'w': update_dictionary})

        # Parameter l (maximum waiting days allowed)

        update_dictionary = {}

        for i in range(n_pats):
            update_dictionary.update({i + 1: patient.max_waiting_days})

        instance.update({'l': update_dictionary})
        
        
        #         self._model.eps = pyo.Param(self._model.I, self._model.K, within=pyo.NonNegativeReals)
        # Parameter esp - adversary realizations

        if self.task.num_adversary_realizations > 0:
            
            update_dictionary = {}
            
            for k in range(self.task.num_adversary_realizations):
                for i in range(n_pats):
                    update_dictionary.update(
                        {(i+1, k+1): 
                            patient.adversary_realization[k]}
                    )

            instance.update({'eps': update_dictionary})
            
        # Parameter day

        update_dictionary = {}
        day = 0
        old_weekday = 0

        for b in range(n_schedule_blocks):
            master_block_index = b % n_master_blocks
            weekday = master_blocks[master_block_index].weekday
            
            if weekday != old_weekday:
                day += 1
                
            old_weekday = weekday
            
            update_dictionary.update({b + 1: day})

        instance.update({'day': update_dictionary})
        
        

        instance.update({
            'n_days': {None: n_days},
            'n_blocks': {None: n_schedule_blocks},
            'n_rooms': {None: n_rooms},
            'n_pats': {None: n_pats},

            # Objective functions coefficients
            'c_exclusion': {None: c_exclusion},
            'c_delay': {None: c_delay},
            
            # TODO controllare se ha senso tenerla
            'n_realizations': {None : self.task.num_adversary_realizations}

            # Covers variables # ANDREBBE RIMOSSA TODO
            # 'covers_excluded': {None: len(covers)},
            # 'different_block_duration': {None: different_block_duration},
        })

        # Pyomo structure requirement - saving among the class members
        self._instance = {None: instance}
        
        self._implementor.instance_data = self._instance


    def run_implementor(self):
        solved_instance = self._implementor.run()
        return Schedule(task = self.task, solved_instance = solved_instance)
        

    def run_adversary(self, schedule):
        # return self.adversary.run(schedule)
        pass

    def update_instance(self, adversary_fragilities):
        # update self.instance_data
        pass



class VanillaImplementor(Optimizer):
    
    
    def __init__(self, task:Task, implementor:Implementor, description = ""):  # implementor:Implementor TODO fix this

        super().__init__(task, description)
        
        # Questo controllo perché chance constraints richiede robustness_overtime
        #if isinstance (implementor, ChanceConstraintsImplementor):
        #self._implementor = implementor(description = "test", robustness_overtime = task.robustness_overtime) # TODO fix this
        #else:
        #    self._implementor = implementor()  # Fix this TODO 

        self._implementor = implementor # TODO add validation and raise error if there is no task argument
        
        self._instance_data = None
        
        self._report = ReportForDirectOptimization(task=task, description=description)


    # Getters and setters

    # Abstract methods implementation
    def run(self):
        
        

        
        # Creating instance
        self.create_instance()
        
        self._report.start_reporting()
                
        #schedule = self._implementor.run()

        solved_instance = self._implementor.run()
        schedule = Schedule(task = self.task, solved_instance = solved_instance)
        
        self._report.end_reporting()
        
        return schedule.export_schedule(), self._report.export_report()

    # Specific methods
    def create_instance(self):
        """
        Qui il metodo è modificato per permettere la chance constraints. Se va modificato va modificato per tutti i tipi di implementor...
        """
        
        master_schedule = self._task.get_master_schedule()
        
        # Parameters for sets
        n_days = self._task.num_of_weeks * master_schedule.get_week_length()
        
        #n_week_days = master_schedule.get_week_length
        n_rooms = master_schedule.get_num_of_rooms()
                    
        c_exclusion = 1  #TODO
        c_delay = 1  #TODO
        
        # Get patients
        patients = self._task.get_patients()
        n_pats = self._task.num_of_patients
        
        # Get master blocks
        master_blocks = master_schedule.get_blocks()
        n_master_blocks = master_schedule.get_num_of_blocks()
        n_schedule_blocks = master_schedule.get_num_of_blocks() * self._task.num_of_weeks 

        # Instance data structure initialization
        instance = {}

        # Parameter g (gamma - capacity)
        update_dictionary = {}

        for b in range(n_schedule_blocks):
            
            master_block_index = b % n_master_blocks

            update_dictionary.update \
                    ({(b + 1): master_blocks[master_block_index].duration })
                
        instance.update({'g': update_dictionary})
        
        # Parameter a (compatibility)

        update_dictionary = {}
        
        for b in range(n_schedule_blocks):
            
            master_block_index = b % n_master_blocks
            
            for i, patient in enumerate(patients):

                patient_equipe = patient.equipe
                block_equipes = master_blocks[master_block_index].equipes
                
                if patient_equipe in block_equipes:
                    update_dictionary.update({(b+1,i+1) : 1})
                else:
                    update_dictionary.update({(b+1,i+1) : 0})

        instance.update({'a': update_dictionary})
        
        # TODO il ciclo sui pazieti potrebbe diventare unico...

        # Parameter t (estimated surgery duration time)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.uncertainty_profile.nominal_value})

        instance.update({'t': update_dictionary})

        # Parameter u (Urgency)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.urgency})

        instance.update({'u': update_dictionary})

        # Parameter w (Waiting days already spent)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.days_waiting})

        instance.update({'w': update_dictionary})

        # Parameter l (maximum waiting days allowed)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.max_waiting_days})

        instance.update({'l': update_dictionary})
        
        # Parameter day

        update_dictionary = {}
        day = 0
        old_weekday = 0

        for b in range(n_schedule_blocks):
            master_block_index = b % n_master_blocks
            weekday = master_blocks[master_block_index].weekday
            
            if weekday != old_weekday:
                day += 1
                
            old_weekday = weekday
            
            update_dictionary.update({b + 1: day})

        instance.update({'day': update_dictionary})
        
        

        
        # Parameter f (percentage point given overtime risk)
        
        update_dictionary = {}
        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.uncertainty_profile.percent_point_function(1-self.task.robustness_risk)})

        instance.update({'f': update_dictionary})

        instance.update({
            'n_days': {None: n_days},
            'n_blocks': {None: n_schedule_blocks},
            'n_rooms': {None: n_rooms},
            'n_pats': {None: n_pats},

            # Objective functions coefficients
            'c_exclusion': {None: c_exclusion},
            'c_delay': {None: c_delay},
            
            # TODO controllare se ha senso tenerla
            'n_realizations': {None : 0}

            # Covers variables # ANDREBBE RIMOSSA TODO
            # 'covers_excluded': {None: len(covers)},
            # 'different_block_duration': {None: different_block_duration},
        })

        # Pyomo structure requirement - saving among the class members
        self._instance = {None: instance}
        
        self._implementor.instance_data = self._instance


    def run_implementor(self):
        solved_instance = self._implementor.run()
        return Schedule(task = self.task, solved_instance = solved_instance)
        



class BudgetSet(Optimizer):

    def __init__(self, task:Task, implementor: Implementor, description = ""):

        super().__init__(task, description)
        
        self._implementor = implementor

        self._instance_data = None
        
        self._report = ReportForDirectOptimization(task=task, description=description)


    # Getters and setters

    #def set_adversary_predictor(self, predictor:PredictiveModel):
    #    self._adversary.predictor = predictor
    #    return True

    # Abstract methods implementation
    def run(self):
        
        self._report.start_reporting()
            
        # param setup    
        for block in self._task.master_schedule.blocks: 

            # List to contain the nominal times of the patients
            patient_times = []

            # Check for patient compatible with the block
            for patient in self._task.patients:                
                if patient.equipe in block.equipes:
                    patient_times.append(patient.uncertainty_profile.nominal_value)
             
            # Calculate parameters   
            times_mean = np.mean(patient_times)
            times_std = np.std(patient_times)/len(patient_times)
            
            block.robustness_budget_set.update({'mean':times_mean,
                                                'std':times_std})
            
            
            for gamma in range(2, self.task.gamma_max +1 ): # inizio da 2 perché se è 1 non posso metterlo a zero

                distribution = ss.norm(loc = gamma*times_mean, scale = times_std)
                
                probability = 1-distribution.cdf(block.duration + self.task.robustness_overtime)
                
                if probability > self.task.robustness_risk:
                    
                    #chosed_gamma  = gamma-1
                    chosed_gamma = gamma + self.task.gamma_variation
                                        
                    block.robustness_budget_set.update({'gamma':chosed_gamma})

        # Now, we add the time increment specifically for each patient
        for patient in self._task.patients:
            percentile = patient.uncertainty_profile.percent_point_function(1-self.task.robustness_risk)  
            time_increment = percentile - patient.uncertainty_profile.nominal_value
            patient.uncertainty_profile.budget_set_time_increment = time_increment
             
                        
        # Creating instance
        self.create_instance()
        
        solved_instance = self._implementor.run()
        
        schedule =  Schedule(task = self.task, 
                             solved_instance = solved_instance)
        
        self._report.end_reporting()
        
        return schedule.export_schedule(), self._report.export_report()
    

        
        

    # Specific methods
    def create_instance(self):
                
        master_schedule = self._task.get_master_schedule()
        
        # Parameters for sets
        n_days = self._task.num_of_weeks * master_schedule.get_week_length()
        
        #n_week_days = master_schedule.get_week_length
        n_rooms = master_schedule.get_num_of_rooms()
                    
        c_exclusion = 1  #TODO
        c_delay = 1  #TODO
        
        # Get patients
        patients = self._task.get_patients()
        n_pats = self._task.num_of_patients
        
        # Get master blocks
        master_blocks = master_schedule.get_blocks()
        n_master_blocks = master_schedule.get_num_of_blocks()
        n_schedule_blocks = master_schedule.get_num_of_blocks() * self._task.num_of_weeks 

        # Instance data structure initialization
        instance = {}

        # Parameter g (gamma - capacity)
        update_dictionary = {}

        for b in range(n_schedule_blocks):
            
            master_block_index = b % n_master_blocks

            update_dictionary.update \
                    ({(b + 1): master_blocks[master_block_index].duration })
                
        instance.update({'g': update_dictionary})
        
        
        update_dictionary = {}
        
        for b in range(n_schedule_blocks):
            
            master_block_index = b % n_master_blocks
            
            update_dictionary.update \
                    ({(b + 1): master_blocks[master_block_index].robustness_budget_set.get('gamma')})
                
        instance.update({'gamma': update_dictionary})
        
        
        # update_dictionary = {}
        
        # for b in range(n_schedule_blocks):
            
        #     master_block_index = b % n_master_blocks

        #     update_dictionary.update \
        #             ({(b + 1): master_blocks[master_block_index].robustness_budget_set.get('time_increment')})
                
        # instance.update({'time_increment': update_dictionary})
        
        update_dictionary = {} # questo è sbagliato: cosa succede se un paziente appartiene a più blocchi?
        for i, patient in enumerate(patients):
            
            update_dictionary.update(
                {(i+1): patient.uncertainty_profile.budget_set_time_increment}
            )
        instance.update({'time_increment': update_dictionary})
        
        
        # Parameter a (compatibility)

        update_dictionary = {}
        
        for b in range(n_schedule_blocks):
            
            master_block_index = b % n_master_blocks
            
            for i, patient in enumerate(patients):

                patient_equipe = patient.equipe
                block_equipes = master_blocks[master_block_index].equipes
                
                if patient_equipe in block_equipes:
                    update_dictionary.update({(b+1,i+1) : 1})
                else:
                    update_dictionary.update({(b+1,i+1) : 0})

        instance.update({'a': update_dictionary})
        
        # TODO il ciclo sui pazieti potrebbe diventare unico...

        # Parameter t (estimated surgery duration time)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.uncertainty_profile.nominal_value})

        instance.update({'t': update_dictionary})

        # Parameter u (Urgency)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.urgency})

        instance.update({'u': update_dictionary})

        # Parameter w (Waiting days already spent)

        update_dictionary = {}

        for i, patient in enumerate(patients):
            update_dictionary.update({i + 1: patient.days_waiting})

        instance.update({'w': update_dictionary})

        # Parameter l (maximum waiting days allowed)

        update_dictionary = {}

        for i in range(n_pats):
            update_dictionary.update({i + 1: patient.max_waiting_days})

        instance.update({'l': update_dictionary})
        
        # Parameter day

        update_dictionary = {}
        day = 0
        old_weekday = 0

        for b in range(n_schedule_blocks):
            master_block_index = b % n_master_blocks
            weekday = master_blocks[master_block_index].weekday
            
            if weekday != old_weekday:
                day += 1
                
            old_weekday = weekday
            
            update_dictionary.update({b + 1: day})

        instance.update({'day': update_dictionary})
        
        #         self._model.eps = pyo.Param(self._model.I, self._model.K, within=pyo.NonNegativeReals)
        # Parameter esp - adversary realizations

        if self.task.num_adversary_realizations > 0:
            
            update_dictionary = {}
            
            for k in range(self.task.num_adversary_realizations):
                for i in range(n_pats):
                    update_dictionary.update(
                        {(i+1, k+1): 
                            patient.adversary_realization[k]}
                    )

            instance.update({'eps': update_dictionary})

        

        instance.update({
            'n_days': {None: n_days},
            'n_blocks': {None: n_schedule_blocks},
            'n_rooms': {None: n_rooms},
            'n_pats': {None: n_pats},
            
            'Gamma' : {None: 4.0},

            # Objective functions coefficients
            'c_exclusion': {None: c_exclusion},
            'c_delay': {None: c_delay},
            
            # TODO controllare se ha senso tenerla
            'n_realizations': {None : self.task.num_adversary_realizations}

            # Covers variables # ANDREBBE RIMOSSA TODO
            # 'covers_excluded': {None: len(covers)},
            # 'different_block_duration': {None: different_block_duration},
        })

        # Pyomo structure requirement - saving among the class members
        self._instance = {None: instance}
        
        self._implementor.instance_data = self._instance




