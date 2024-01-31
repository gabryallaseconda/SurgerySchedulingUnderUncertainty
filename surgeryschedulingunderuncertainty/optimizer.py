
from dotenv import load_dotenv
load_dotenv()
import os 

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
    

class StandardImplementor(ABC):

    def __init__(self, instance_data, description = ""):
        super().__init(instance_data, description)

            
        # Create a Pyomo Abstract Model, to be filled
        model = pyo.AbstractModel()

        # Sets
        model.n_days = pyo.Param(default=2,
                                doc="Number of days filled by the schedule"
                                )
        model.D = pyo.RangeSet(1,
                            model.n_days
                            )

        model.n_rooms = pyo.Param(default=2,
                                doc="Number of available operating rooms"
                                )
        model.J = pyo.RangeSet(1,
                            model.n_rooms
                            )

        model.n_blocks = pyo.Param(default=2,
                                doc="Number of surgery specialties blocks"
                                )
        model.B = pyo.RangeSet(1,
                            model.n_blocks
                            )

        model.n_pats = pyo.Param(default=12,
                                doc="Nuber of patients"
                                )
        model.I = pyo.RangeSet(1,
                            model.n_pats
                            )

        model.n_realizations = pyo.Param(default=0,
                                        doc="Number of implementor/adversary iterations"
                                        )
        model.K = pyo.RangeSet(1,
                            model.n_realizations
                            )

        # Parameters
        model.t = pyo.Param(model.I,
                            default=0,
                            doc="expected surgery time, given in minutes"
                            )

        model.eps = pyo.Param(model.I,
                            model.K,
                            default=0,
                            doc="additional time of overtime for each implementor iteration"
                            )

        model.w = pyo.Param(model.I,
                            default=0,
                            doc="day weited in queue by the patient, given in days"
                            )

        model.l = pyo.Param(model.I,
                            default=0,
                            doc="maximum number of days before the surgery, from queue entry"
                            )

        model.u = pyo.Param(model.I,
                            default=0,
                            doc="urgency parameter"
                            )

        model.g = pyo.Param(model.D,
                            model.J,
                            model.B,
                            default=0,
                            within=pyo.NonNegativeIntegers,
                            doc="total block time"
                            )

        model.a = pyo.Param(model.D,
                            model.J,
                            model.B,
                            model.I,
                            within=pyo.Binary,
                            doc="compatibility block-patient"
                            )

        model.c_exclusion = pyo.Param(default=1,
                                    doc="penalty for not scheduled patients"
                                    )

        model.c_delay = pyo.Param(default=1,
                                doc="penalty for patient processed after the maximum time"
                                )

        # Variables
        model.x = pyo.Var(model.D,
                        model.J,
                        model.B,
                        model.I,
                        within=pyo.Binary
                        )

        model.y = pyo.Var(model.I,
                        within=pyo.NonNegativeReals
                        )

        model.z = pyo.Var(model.I,
                        within=pyo.NonNegativeReals
                        )

        # Objective function
        def ObjRule_standard(model):
            return pyo.summation(model.u, model.y) + \
                sum((1 - sum(model.x[d, j, b, i] for d in model.D for j in model.J for b in model.B)) * model.u[i] for i in
                    model.I) * model.c_exclusion + \
                pyo.summation(model.u, model.z) * model.c_delay

        def ObjRule_count(model):
            return pyo.summation(model.x)

        # todo: make the following
        # altra funzione obiettivo che sia la massimizzazione della somma delle x, da testare con un orizzonte temporale variabile
        # minimizzazione del makespan - ultimo giorno in cui uno viene operato per ciascuna specialità.

        if objective_setting == 'standard':
            model.obj = pyo.Objective(rule=ObjRule_standard,
                                    sense=pyo.minimize)
        elif objective_setting == 'count':
            model.obj = pyo.Objective(rule=ObjRule_count,
                                    sense=pyo.maximize)
        else:
            raise ValueError('Objective setting not admitted')

        # Constraints
        def delayDetectorRule(model, i):
            return model.y[i] + model.w[i] - model.l[i] <= model.z[i]

        model.delayDetector = pyo.Constraint(model.I,
                                            rule=delayDetectorRule
                                            )

        #TODO: questa potrebbe essere rimossa?
        def capacityRule(model, d, j, b):
            return sum(model.x[d, j, b, i] * model.t[i] for i in model.I) <= model.g[d, j, b]

        model.capacity = pyo.Constraint(model.D,
                                        model.J,
                                        model.B,
                                        rule=capacityRule
                                        )

        def capacityOvertimeRule(model, d, j, b, k):
            return sum(model.x[d, j, b, i] * (model.t[i] + model.eps[i, k]) for i in model.I) <= model.g[d, j, b]

        model.capacityOvertime = pyo.Constraint(model.D,
                                                model.J,
                                                model.B,
                                                model.K,
                                                rule=capacityOvertimeRule
                                                )

        def compatibilityRule(model, d, j, b, i):
            return model.x[d, j, b, i] <= model.a[d, j, b, i]

        model.compatibility = pyo.Constraint(model.D,
                                            model.J,
                                            model.B,
                                            model.I,
                                            rule=compatibilityRule
                                            )

        def oneSurgeryRule(model, i):
            return sum(model.x[d, j, b, i] for j in model.J for d in model.D for b in model.B) <= 1

        model.oneSurgery = pyo.Constraint(model.I,
                                        rule=oneSurgeryRule
                                        )

        def YVarDefRule(model, i):
            return model.y[i] == sum(d * model.x[d, j, b, i] for d in model.D for j in model.J for b in model.B) + \
                (model.n_days + 1) * (1 - sum(model.x[d, j, b, i] for d in model.D for j in model.J for b in model.B))

        model.YVarDef = pyo.Constraint(model.I,
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

        return self.instance





    
