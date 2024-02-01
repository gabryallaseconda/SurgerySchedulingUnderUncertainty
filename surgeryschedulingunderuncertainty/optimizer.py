
from dotenv import load_dotenv
load_dotenv()
import os 

# ABstract Classes
from abc import ABC, abstractmethod

# Package for mathematical programming modelling
import pyomo.environ as pyo


class Optimizer(ABC):
    
    def __init__(self, task, description = ""):
        self.tast = task
        self.description = ""

        self.schedule = None


    @task.getter
    def task(self):
        return self.task
    
    @task.setter
    def task(self, new_task):
        self.task = new_task

    
    @description.getter
    def description(self):
        return self.description
    
    @description.setter
    def description(self, new_description):
        self.description = new_description
    

    @abstractmethod
    def run():
        pass
    


####################
#### Optimizer: implementor adversary

class ImplementorAdversary(PatientProvider):

    def __init__(self, task, implementor, adversary, description = ""):

        super().__init__(task, description)
        
        self.implementor = implementor
        self.adversary = adversary

        self.instance_data = None



    def set_adversary_predictor(self, predictor):
        self.adversary.predictor = predictor
        return True


    def run(self, max_loops = 0):
        # Setting the number of max loops. If not setted then load it from environment variable.
        if max_loops == 0:
            max_loops = os.environ.get("MAXIMUM_IMPLEMENTOR_ADVERSARY_LOOPS")

        # Main implementor adversary loop
        for loop in range(max_loops):
            flag = False

            # call implementor


            # call adversary

            if flag == True:
                break

            # update instance data

        
        #return schedule


    def create_instance_data(self):
        pass

    def run_implementor(self, instance_data):
        # return self.implementor.run(instance_data)
        pass

    def run_adversary(self, schedule):
        # return self.adversary.run(schedule)
        pass

    def update_instance_data(self, adversary_fragilities):
        # update self.instance_data
        pass



class Implementor(ABC):
    
    def __init__(self, instance_data, description = ""):
        self.instance_data = instance_data
        self.description = description
        
        self.model = None

    @schedule.getter
    def schedule(self):
        return self.schedule
    
    @schedule.setter
    def schedule(self, new_schedule):
        self.schedule = new_schedule
    

    @instance_data.getter
    def instance_data(self):
        return self.instance_data
    
    @instance_data.setter
    def instance_data(self, new_instance_data):
        self.instance_data = new_instance_data


    @abstractmethod
    def run(self):
        pass
    

class StandardImplementor():

    def __init__(self, instance_data, description = ""):
        super().__init(instance_data, description)

            
        # Create a Pyomo Abstract Model, to be filled
        self.model = pyo.AbstractModel()

        # Sets
        self.model.n_days = pyo.Param(default=2,
                                doc="Number of days filled by the schedule"
                                )
        self.model.D = pyo.RangeSet(1,
                            self.model.n_days
                            )

        self.model.n_rooms = pyo.Param(default=2,
                                doc="Number of available operating rooms"
                                )
        self.model.J = pyo.RangeSet(1,
                            self.model.n_rooms
                            )

        self.model.n_blocks = pyo.Param(default=2,
                                doc="Number of surgery specialties blocks"
                                )
        self.model.B = pyo.RangeSet(1,
                            self.model.n_blocks
                            )

        self.model.n_pats = pyo.Param(default=12,
                                doc="Nuber of patients"
                                )
        self.model.I = pyo.RangeSet(1,
                            self.model.n_pats
                            )

        self.model.n_realizations = pyo.Param(default=0,
                                        doc="Number of implementor/adversary iterations"
                                        )
        self.model.K = pyo.RangeSet(1,
                            self.model.n_realizations
                            )

        # Parameters
        self.model.t = pyo.Param(self.model.I,
                            default=0,
                            doc="expected surgery time, given in minutes"
                            )

        self.model.eps = pyo.Param(self.model.I,
                            self.model.K,
                            default=0,
                            doc="additional time of overtime for each implementor iteration"
                            )

        self.model.w = pyo.Param(self.model.I,
                            default=0,
                            doc="day weited in queue by the patient, given in days"
                            )

        self.model.l = pyo.Param(self.model.I,
                            default=0,
                            doc="maximum number of days before the surgery, from queue entry"
                            )

        self.model.u = pyo.Param(self.model.I,
                            default=0,
                            doc="urgency parameter"
                            )

        self.model.g = pyo.Param(self.model.D,
                            self.model.J,
                            self.model.B,
                            default=0,
                            within=pyo.NonNegativeIntegers,
                            doc="total block time"
                            )

        self.model.a = pyo.Param(self.model.D,
                            self.model.J,
                            self.model.B,
                            self.model.I,
                            within=pyo.Binary,
                            doc="compatibility block-patient"
                            )

        self.model.c_exclusion = pyo.Param(default=1,
                                    doc="penalty for not scheduled patients"
                                    )

        self.model.c_delay = pyo.Param(default=1,
                                doc="penalty for patient processed after the maximum time"
                                )

        # Variables
        self.model.x = pyo.Var(self.model.D,
                        self.model.J,
                        self.model.B,
                        self.model.I,
                        within=pyo.Binary
                        )

        self.model.y = pyo.Var(self.model.I,
                        within=pyo.NonNegativeReals
                        )

        self.model.z = pyo.Var(self.model.I,
                        within=pyo.NonNegativeReals
                        )

        # Objective function
        def ObjRule_standard(self):
            return pyo.summation(self.model.u, self.model.y) + \
                sum((1 - sum(self.model.x[d, j, b, i] for d in self.model.D for j in self.model.J for b in self.model.B)) * self.model.u[i] for i in
                    self.model.I) * self.model.c_exclusion + \
                pyo.summation(self.model.u, self.model.z) * self.model.c_delay
        
        self.model.obj = pyo.Objective(rule=ObjRule_standard,
                                    sense=pyo.minimize)
        
        # Constraints
        def delayDetectorRule(self, i):
            return self.model.y[i] + self.model.w[i] - self.model.l[i] <= self.model.z[i]

        self.model.delayDetector = pyo.Constraint(self.model.I,
                                            rule=delayDetectorRule
                                            )

        #TODO: questa potrebbe essere rimossa?
        def capacityRule(self, d, j, b):
            return sum(self.model.x[d, j, b, i] * self.model.t[i] for i in self.model.I) <= self.model.g[d, j, b]

        self.model.capacity = pyo.Constraint(self.model.D,
                                        self.model.J,
                                        self.model.B,
                                        rule=capacityRule
                                        )

        def capacityOvertimeRule(self, d, j, b, k):
            return sum(self.model.x[d, j, b, i] * (self.model.t[i] + self.model.eps[i, k]) for i in self.model.I) <= self.model.g[d, j, b]

        self.model.capacityOvertime = pyo.Constraint(self.model.D,
                                                self.model.J,
                                                self.model.B,
                                                self.model.K,
                                                rule=capacityOvertimeRule
                                                )

        def compatibilityRule(self, d, j, b, i):
            return self.model.x[d, j, b, i] <= self.model.a[d, j, b, i]

        self.model.compatibility = pyo.Constraint(self.model.D,
                                            self.model.J,
                                            self.model.B,
                                            self.model.I,
                                            rule=compatibilityRule
                                            )

        def oneSurgeryRule(self, i): # one surgery
            return sum(self.model.x[d, j, b, i] for j in self.model.J for d in self.model.D for b in self.model.B) <= 1

        self.model.oneSurgery = pyo.Constraint(self.model.I,
                                        rule=oneSurgeryRule
                                        )

        def YVarDefRule(self, i): # Y variable definition
            return self.model.y[i] == sum(d * self.model.x[d, j, b, i] for d in self.model.D for j in self.model.J for b in self.model.B) + \
                (self.model.n_days + 1) * (1 - sum(self.model.x[d, j, b, i] for d in self.model.D for j in self.model.J for b in self.model.B))

        self.model.YVarDef = pyo.Constraint(self.model.I,
                                    rule=YVarDefRule)
        
    
    def run(self):
        # Instance creation
        self.instance = self.model.create_instance(self.instance_data)

        # Solver configuration
        solver = pyo.SolverFactory('appsi_highs')

        #solver.options['Threads'] = config['SOLVER']['SolverThreads']
        #solver.options['TimeLimit'] = config['SOLVER']['SolverTimeLimit']
        #solver.options['MIPGap'] = config['SOLVER']['SolverMIPGap']

        #TODO questo path andrebbe dedotto, non hard-coded
        path = '/Users/gabrielegabrielli/Library/CloudStorage/OneDrive-PolitecnicodiMilano/PoliMi/Tesi/PianificazioneRobustaInterventiChirurgici REAL/output_data/'
        filename = 'highs_log_' + instance_name + '.txt' #.replace(',','').replace(' ','').replace('(','').replace(')','').replace('.','')
        solver.options['LogFile'] = path + filename

        # Solver launching
        solver_result = solver.solve(self.instance, tee=False)  # sicuri che qua servono tutti e due?
        # Saving data of the solution
        self.instance.solutions.store_to(solver_result)

        return self.instance # questa adrebbe processata dentro una schedula prima di procedere



class CountingImplementor():

    def __init__(self, instance_data, description = ""):
        super().__init(instance_data, description)

            
        # Create a Pyomo Abstract Model, to be filled
        self.model = pyo.AbstractModel()

        # Sets
        self.model.n_days = pyo.Param(default=2,
                                doc="Number of days filled by the schedule"
                                )
        self.model.D = pyo.RangeSet(1,
                            self.model.n_days
                            )

        self.model.n_rooms = pyo.Param(default=2,
                                doc="Number of available operating rooms"
                                )
        self.model.J = pyo.RangeSet(1,
                            self.model.n_rooms
                            )

        self.model.n_blocks = pyo.Param(default=2,
                                doc="Number of surgery specialties blocks"
                                )
        self.model.B = pyo.RangeSet(1,
                            self.model.n_blocks
                            )

        self.model.n_pats = pyo.Param(default=12,
                                doc="Nuber of patients"
                                )
        self.model.I = pyo.RangeSet(1,
                            self.model.n_pats
                            )

        self.model.n_realizations = pyo.Param(default=0,
                                        doc="Number of implementor/adversary iterations"
                                        )
        self.model.K = pyo.RangeSet(1,
                            self.model.n_realizations
                            )

        # Parameters
        self.model.t = pyo.Param(self.model.I,
                            default=0,
                            doc="expected surgery time, given in minutes"
                            )

        self.model.eps = pyo.Param(self.model.I,
                            self.model.K,
                            default=0,
                            doc="additional time of overtime for each implementor iteration"
                            )

        self.model.w = pyo.Param(self.model.I,
                            default=0,
                            doc="day weited in queue by the patient, given in days"
                            )

        self.model.l = pyo.Param(self.model.I,
                            default=0,
                            doc="maximum number of days before the surgery, from queue entry"
                            )

        self.model.u = pyo.Param(self.model.I,
                            default=0,
                            doc="urgency parameter"
                            )

        self.model.g = pyo.Param(self.model.D,
                            self.model.J,
                            self.model.B,
                            default=0,
                            within=pyo.NonNegativeIntegers,
                            doc="total block time"
                            )

        self.model.a = pyo.Param(self.model.D,
                            self.model.J,
                            self.model.B,
                            self.model.I,
                            within=pyo.Binary,
                            doc="compatibility block-patient"
                            )

        self.model.c_exclusion = pyo.Param(default=1,
                                    doc="penalty for not scheduled patients"
                                    )

        self.model.c_delay = pyo.Param(default=1,
                                doc="penalty for patient processed after the maximum time"
                                )

        # Variables
        self.model.x = pyo.Var(self.model.D,
                        self.model.J,
                        self.model.B,
                        self.model.I,
                        within=pyo.Binary
                        )

        self.model.y = pyo.Var(self.model.I,
                        within=pyo.NonNegativeReals
                        )

        self.model.z = pyo.Var(self.model.I,
                        within=pyo.NonNegativeReals
                        )

        # Objective function
        def ObjRule_count(self):
            return pyo.summation(self.model.x)

        self.model.obj = pyo.Objective(rule=ObjRule_count,
                                    sense=pyo.maximize)

        # Constraints
        def delayDetectorRule(self, i):
            return self.model.y[i] + self.model.w[i] - self.model.l[i] <= self.model.z[i]

        self.model.delayDetector = pyo.Constraint(self.model.I,
                                            rule=delayDetectorRule
                                            )

        #TODO: questa potrebbe essere rimossa?
        def capacityRule(self, d, j, b):
            return sum(self.model.x[d, j, b, i] * self.model.t[i] for i in self.model.I) <= self.model.g[d, j, b]

        self.model.capacity = pyo.Constraint(self.model.D,
                                        self.model.J,
                                        self.model.B,
                                        rule=capacityRule
                                        )

        def capacityOvertimeRule(self, d, j, b, k):
            return sum(self.model.x[d, j, b, i] * (self.model.t[i] + self.model.eps[i, k]) for i in self.model.I) <= self.model.g[d, j, b]

        self.model.capacityOvertime = pyo.Constraint(self.model.D,
                                                self.model.J,
                                                self.model.B,
                                                self.model.K,
                                                rule=capacityOvertimeRule
                                                )

        def compatibilityRule(self, d, j, b, i):
            return self.model.x[d, j, b, i] <= self.model.a[d, j, b, i]

        self.model.compatibility = pyo.Constraint(self.model.D,
                                            self.model.J,
                                            self.model.B,
                                            self.model.I,
                                            rule=compatibilityRule
                                            )

        def oneSurgeryRule(self, i): # one surgery
            return sum(self.model.x[d, j, b, i] for j in self.model.J for d in self.model.D for b in self.model.B) <= 1

        self.model.oneSurgery = pyo.Constraint(self.model.I,
                                        rule=oneSurgeryRule
                                        )

        def YVarDefRule(self, i): # Y variable definition
            return self.model.y[i] == sum(d * self.model.x[d, j, b, i] for d in self.model.D for j in self.model.J for b in self.model.B) + \
                (self.model.n_days + 1) * (1 - sum(self.model.x[d, j, b, i] for d in self.model.D for j in self.model.J for b in self.model.B))

        self.model.YVarDef = pyo.Constraint(self.model.I,
                                    rule=YVarDefRule)
        
    
    def run(self):
        # Instance creation
        self.instance = self.model.create_instance(self.instance_data)

        # Solver configuration
        solver = pyo.SolverFactory('appsi_highs')

        #solver.options['Threads'] = config['SOLVER']['SolverThreads']
        #solver.options['TimeLimit'] = config['SOLVER']['SolverTimeLimit']
        #solver.options['MIPGap'] = config['SOLVER']['SolverMIPGap']

        #TODO questo path andrebbe dedotto, non hard-coded
        path = '/Users/gabrielegabrielli/Library/CloudStorage/OneDrive-PolitecnicodiMilano/PoliMi/Tesi/PianificazioneRobustaInterventiChirurgici REAL/output_data/'
        filename = 'highs_log_' + instance_name + '.txt' #.replace(',','').replace(' ','').replace('(','').replace(')','').replace('.','')
        solver.options['LogFile'] = path + filename

        # Solver launching
        solver_result = solver.solve(self.instance, tee=False)  # sicuri che qua servono tutti e due?
        # Saving data of the solution
        self.instance.solutions.store_to(solver_result)

        return self.instance # questa adrebbe processata dentro una schedula prima di procedere



def Adversary(ABC): # da completare
    def __init__(self, predictor, schedule, description = ""):
        self.predictor = predictor
        self.schedule = schedule
        self.description = description
        

    @schedule.getter
    def schedule(self):
        return self.schedule
    
    @schedule.setter
    def schedule(self, new_schedule):
        self.schedule = new_schedule
    

    @instance_data.getter
    def instance_data(self):
        return self.instance_data
    
    @instance_data.setter
    def instance_data(self, new_instance_data):
        self.instance_data = new_instance_data


    @abstractmethod
    def run(self):
        pass
    