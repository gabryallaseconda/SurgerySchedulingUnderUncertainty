# Python STL
from abc import ABC, abstractmethod

# Packages
import pyomo.environ as pyo


# Objective function
def ObjRule_standard(self):
    return pyo.summation(self.model.u, self.model.y) + \
        sum((1 - sum(self.model.x[d, j, b, i] for d in self.model.D for j in self.model.J for b in self.model.B)) * self.model.u[i] for i in
            self.model.I) * self.model.c_exclusion + \
        pyo.summation(self.model.u, self.model.z) * self.model.c_delay

def ObjRule_count(self):
    return pyo.summation(self.model.x)

# Constraints
def delayDetectorRule(self, i):
    return self.model.y[i] + self.model.w[i] - self.model.l[i] <= self.model.z[i]

def capacityRule(self, d, j, b):
    return sum(self.model.x[d, j, b, i] * self.model.t[i] for i in self.model.I) <= self.model.g[d, j, b]

def capacityOvertimeRule(self, d, j, b, k):
    return sum(self.model.x[d, j, b, i] * (self.model.t[i] + self.model.eps[i, k]) for i in self.model.I) <= self.model.g[d, j, b]

def compatibilityRule(self, d, j, b, i):
    return self.model.x[d, j, b, i] <= self.model.a[d, j, b, i]

def oneSurgeryRule(self, i): # one surgery
    return sum(self.model.x[d, j, b, i] for j in self.model.J for d in self.model.D for b in self.model.B) <= 1

def YVarDefRule(self, i): # Y variable definition
    return self.model.y[i] == sum(d * self.model.x[d, j, b, i] for d in self.model.D for j in self.model.J for b in self.model.B) + \
                (self.model.n_days + 1) * (1 - sum(self.model.x[d, j, b, i] for d in self.model.D for j in self.model.J for b in self.model.B))


class Implementor(ABC):
    
    def __init__(self, instance_data, description = ""):
        self.instance_data = instance_data
        self.description = description
        
        # Pyomo Abstract Model
        self.model = pyo.AbstractModel()

    # Getters and setters
        
    def get_schedule(self):
        return self._schedule
    
    def set_schedule(self, new):
        self.schedule = new

    schedule = property(get_schedule, set_schedule)
    

    def get_instance_data(self):
        return self._instance_data
    
    def set_instance_data(self, new):
        self._instance_data = new

    instance_data = property(get_instance_data, set_instance_data)

    # Abstract methods

    # Common methods
    def run(self): #!!!!!
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
    
    

class StandardImplementor():

    def __init__(self, instance_data, description = ""):
        super().__init(instance_data, description)

        # Sets
        self.model.n_days = pyo.Param()
        self.model.n_rooms = pyo.Param()
        self.model.n_blocks = pyo.Param()
        self.model.n_pats = pyo.Param()
        self.model.n_realizations = pyo.Param()

        self.model.D = pyo.RangeSet(1, self.model.n_days)
        self.model.J = pyo.RangeSet(1, self.model.n_rooms)
        self.model.B = pyo.RangeSet(1, self.model.n_blocks)
        self.model.I = pyo.RangeSet(1, self.model.n_pats)
        self.model.K = pyo.RangeSet(1, self.model.n_realizations)

        # Parameters
        self.model.t = pyo.Param(self.model.I)
        self.model.w = pyo.Param(self.model.I)
        self.model.l = pyo.Param(self.model.I)
        self.model.u = pyo.Param(self.model.I)

        self.model.eps = pyo.Param(self.model.I, self.model.K)

        self.model.g = pyo.Param(self.model.D, self.model.J, self.model.B, within=pyo.NonNegativeIntegers)
        self.model.a = pyo.Param(self.model.D, self.model.J, self.model.B, self.model.I, within=pyo.Binary)

        self.model.c_exclusion = pyo.Param()
        self.model.c_delay = pyo.Param()

        # Variables
        self.model.x = pyo.Var(self.model.D, self.model.J, self.model.B, self.model.I, within=pyo.Binary)
        self.model.y = pyo.Var(self.model.I, within=pyo.NonNegativeReals)
        self.model.z = pyo.Var(self.model.I, within=pyo.NonNegativeReals)

        # Objective function
        self.model.obj = pyo.Objective(rule=ObjRule_standard, sense=pyo.minimize)
        
        # Constraints
        self.model.delayDetector = pyo.Constraint(self.model.I, rule=delayDetectorRule)
        self.model.capacity = pyo.Constraint(self.model.D, self.model.J, self.model.B, rule=capacityRule)
        self.model.capacityOvertime = pyo.Constraint(self.model.D, self.model.J, self.model.B, self.model.K, rule=capacityOvertimeRule)
        self.model.compatibility = pyo.Constraint(self.model.D, self.model.J, self.model.B, self.model.I, rule=compatibilityRule)
        self.model.oneSurgery = pyo.Constraint(self.model.I, rule=oneSurgeryRule)
        self.model.YVarDef = pyo.Constraint(self.model.I, rule=YVarDefRule)
        
    

class CountingImplementor():

    def __init__(self, instance_data, description = ""):
        super().__init(instance_data, description)

        # Sets
        self.model.n_days = pyo.Param()
        self.model.n_rooms = pyo.Param()
        self.model.n_blocks = pyo.Param()
        self.model.n_pats = pyo.Param()
        self.model.n_realizations = pyo.Param()

        self.model.D = pyo.RangeSet(1, self.model.n_days)
        self.model.J = pyo.RangeSet(1, self.model.n_rooms)
        self.model.B = pyo.RangeSet(1, self.model.n_blocks)
        self.model.I = pyo.RangeSet(1, self.model.n_pats)
        self.model.K = pyo.RangeSet(1, self.model.n_realizations)

        # Parameters
        self.model.t = pyo.Param(self.model.I)
        self.model.w = pyo.Param(self.model.I)
        self.model.l = pyo.Param(self.model.I)
        self.model.u = pyo.Param(self.model.I)

        self.model.eps = pyo.Param(self.model.I, self.model.K)

        self.model.g = pyo.Param(self.model.D, self.model.J, self.model.B, within=pyo.NonNegativeIntegers)
        self.model.a = pyo.Param(self.model.D, self.model.J, self.model.B, self.model.I, within=pyo.Binary)

        self.model.c_exclusion = pyo.Param()
        self.model.c_delay = pyo.Param()

        # Variables
        self.model.x = pyo.Var(self.model.D, self.model.J, self.model.B, self.model.I, within=pyo.Binary)
        self.model.y = pyo.Var(self.model.I, within=pyo.NonNegativeReals)
        self.model.z = pyo.Var(self.model.I, within=pyo.NonNegativeReals)

        # Objective function
        self.model.obj = pyo.Objective(rule=ObjRule_count, sense=pyo.maximize)

        # Constraints
        self.model.delayDetector = pyo.Constraint(self.model.I, rule=delayDetectorRule)
        self.model.capacity = pyo.Constraint(self.model.D, self.model.J, self.model.B, rule=capacityRule)
        self.model.capacityOvertime = pyo.Constraint(self.model.D, self.model.J, self.model.B, self.model.K, rule=capacityOvertimeRule)
        self.model.compatibility = pyo.Constraint(self.model.D, self.model.J, self.model.B, self.model.I, rule=compatibilityRule)
        self.model.oneSurgery = pyo.Constraint(self.model.I, rule=oneSurgeryRule)
        self.model.YVarDef = pyo.Constraint(self.model.I, rule=YVarDefRule)