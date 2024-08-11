# Python STL
from abc import ABC, abstractmethod
from datetime import datetime

# Packages
import pyomo.environ as pyo  # not used for the implementor adversary
import numpy as np
import scipy.stats as ss

# Modules
from .implementor import Implementor, ChanceConstraintsImplementor
from .adversary import Adversary, EquiprobableVertex
from .task import Task
from .predictive_model import PredictiveModel
from .schedule import Schedule



class Report(ABC):
    
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
    def export_report():
        pass
    
    

class ReportForImplementorAdversary(Report):

    def __init__(self, task:Task, description = ""):

        super().__init__(task, description)
        
        self._start_time = None
        self._end_time = None
        
        self._start_iterations_time = None
        
        self._total_time = 0
        self._n_iterations = 0
        self._list_of_iterations_times = []
        self._list_of_iterations_durations = []
        self._list_of_iterations_flags = []
        
        
    def start_reporting(self):
        if self._start_time is not None:
            raise ValueError("Reporting can be started only once.")
        
        self._start_time = datetime.now()
        
        
    def end_reporting(self):
        if self._start_time is None:
            raise ValueError("Reporting must be started before being ended.")
        if self._end_time is not None:
            raise ValueError("Reporting can be ended only once.")
        
        self._end_time = datetime.now()
        print(self._end_time)
        print(self._start_time)
        self._total_time = (self._end_time - self._start_time).total_seconds() / 60
        print(self._total_time)
        
    def start_iterations_reporting(self):
        if self._start_iterations_time is not None:
            raise ValueError("Iteration reporting can be started only once.")
        self._start_iterations_time = datetime.now()            
        
    def report_iteration(self, flag):
        
        if self._start_iterations_time is None:
            raise ValueError("Iteration reporting must be started before report iterations.")
        
        self._list_of_iterations_times.append(datetime.now())
        self._list_of_iterations_flags.append(flag)
        
        if len(self._list_of_iterations_times) == 1:
            duration = (self._list_of_iterations_times[0] - self._start_iterations_time).total_seconds() / 60
        else:
            duration = (self._list_of_iterations_times[-1] - self._list_of_iterations_times[-2]).total_seconds() / 60            
        
        self._list_of_iterations_durations.append(duration)
        
        self._n_iterations += 1
    
    def export_report(self):
        
        data_dictionary = {
            'total duration': self._total_time,
            'start time': self._start_time,
            'end time': self._end_time,
            'number of iterations' : len(self._list_of_iterations_flags),
            'is last robust' : 'Yes' if self._list_of_iterations_flags[-1] else 'No',
            'iterations':[]
        }
        
        for iteration in range(len(self._list_of_iterations_flags)):
            data_dictionary['iterations'].append({
                'flag': self._list_of_iterations_flags[iteration],
                'duration': self._list_of_iterations_durations[iteration]
            }
            )
            
        return data_dictionary
        
    

class ReportForDirectOptimization(Report):

    def __init__(self, task:Task, description = ""):

        super().__init__(task, description)
        
        self._start_time = None
        self._end_time = None
                
        self._total_time = 0

        
        
    def start_reporting(self):
        if self._start_time is not None:
            raise ValueError("Reporting can be started only once.")
        self._start_time = datetime.now()
        
    def end_reporting(self):
        if self._start_time is None:
            raise ValueError("Reporting must be started before being ended.")
        if self._end_time is not None:
            raise ValueError("Reporting can be ended only once.")
        self._end_time = datetime.now()
        self._total_time = (self._end_time - self._start_time).total_seconds() / 60

    def export_report(self):
        
        data_dictionary = {
            'total duration': self._total_time,
            'start time': self._start_time,
            'end time': self._end_time,
        }
            
        return data_dictionary
        

