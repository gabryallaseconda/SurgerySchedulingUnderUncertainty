# Packages
import pyomo.environ as pyo


# Objective function
#def ObjRule_standard(self):
#    return pyo.summation(self._model.u, self._model.y) + \
#        sum((1 - sum(self._model.x[d, j, b, i] for d in self._model.D for j in self._model.J for b in self._model.B)) * self._model.u[i] for i in
#            self._model.I) * self._model.c_exclusion + \
#        pyo.summation(self._model.u, self._model.z) * self._model.c_delay
def ObjRule_standard(model):
    return pyo.summation(model.u, model.y) + \
        sum((1 - sum(model.x[b, i]  for b in model.B)) * model.u[i] for i in
            model.I) * model.c_exclusion + \
        pyo.summation(model.u, model.z) * model.c_delay

def ObjRule_count(model):
    return pyo.summation(model.x)

# Constraints
def delayDetectorRule(model, i):
    return model.y[i] + model.w[i] - model.l[i] <= model.z[i]

#def capacityRule(self, d, j, b):
#    return sum(self._model.x[d, j, b, i] * self._model.t[i] for i in self._model.I) <= self._model.g[d, j, b]

#def capacityOvertimeRule(self, d, j, b, k):
#    return sum(self._model.x[d, j, b, i] * (self._model.t[i] + self._model.eps[i, k]) for i in self._model.I) <= self._model.g[d, j, b]

#def compatibilityRule(self, d, j, b, i):
#    return self._model.x[d, j, b, i] <= self._model.a[d, j, b, i]

def capacityRule(model, b):
    return sum(model.x[b, i] * model.t[i] for i in model.I) <= model.g[b]

def capacityOvertimeRule(model, b, k):
    return sum(model.x[b, i] * (model.t[i] + model.eps[i, k]) for i in model.I) <= model.g[b]

def compatibilityRule(model, b, i):
    return model.x[b, i] <= model.a[b, i]


#def oneSurgeryRule(self, i): # one surgery
#    return sum(self._model.x[d, j, b, i] for j in self._model.J for d in self._model.D for b in self._model.B) <= 1

#def YVarDefRule(self, i): # Y variable definition
#    return self._model.y[i] == sum(d * self._model.x[d, j, b, i] for d in self._model.D for j in self._model.J for b in self._model.B) + \
#                (self._model.n_days + 1) * (1 - sum(self._model.x[d, j, b, i] for d in self._model.D for j in self._model.J for b in self._model.B))

def oneSurgeryRule(model, i): # one surgery
    return sum(model.x[b, i] for b in model.B) <= 1

def YVarDefRule(model, i): # Y variable definition # TODO: sistemare questo scempio. cosa fare se i giorni contengono un numero diverso di blocchi?
    return model.y[i] == sum( (int(b/ (model.n_blocks/model.n_days) )+1) * model.x[b, i] for b in model.B) + \
                (model.n_days + 1) * (1 - sum(model.x[b, i] for b in model.B))

# Chance Constraints - Time Extension variable q

def fractionSumOneRule(model, b): 
    return sum(model.q[b,i] for i in model.I) <= 1

def assignmentExistRule(model, b, i):
    return model.q[b,i] <= model.x[b,i]

def chanceConstraintRule(robustness_overtime):
    def internalRule(model, b, i): 
        return (model.g[b]+robustness_overtime)*model.q[b,i] >= model.f[i]
    return internalRule
