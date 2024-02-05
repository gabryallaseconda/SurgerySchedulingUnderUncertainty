
from abc import ABC, abstractmethod

#from patient import Patient


class Block(ABC):
    
    def __init__(self, duration: int, equipes: list[str], weekday: int, order_in_day: int):
        self.duration = duration
        self.equipes = equipes
        self.weekday = weekday
        self.order_in_day = order_in_day

    # Getters and setters
    def get_duration(self):
        return self._duration
    
    def set_duration(self, new:int):
        self._duration = new
    
    duration = property(get_duration, set_duration)

    def get_equipes(self):
        return self._equipes
    
    def set_equipes(self, new: list[str]):
        self._equipes = new
    
    equipes = property(get_equipes, set_equipes)

    def get_weekday(self):
        return self._weekday
    
    def set_weekday(self, new: int):
        self._weekday = new
    
    weekday = property(get_weekday, set_weekday)

    def get_order_in_day(self):
        return self._order_in_day
    
    def set_order_in_day(self, new: int):
        self._order_in_day = new
    
    order_in_day = property(get_order_in_day, set_order_in_day)




class MasterBlock(Block):

    def __init__(self, duration: int, equipes: list[str], weekday: int, order_in_day: int, order_in_master: int):
        super().__init__(duration, equipes, weekday, order_in_day)
        self.order_in_master = order_in_master

    def get_order_in_master(self):
        return self._order_in_master
    
    def set_order_in_master(self, new:int):
        self._order_in_master = new
    
    order_in_master = property(get_order_in_master, set_order_in_master)



# class ScheduleBlock(Block):

#     def __init__(self, duration: int, equipes: list[str], weekday: int, order_in_day: int, 
#                  order_in_week: int, order_in_schedule: int, patients: list[Patient] = None):
#         super().__init__(duration, equipes, weekday, order_in_day)
#         self.order_in_week = order_in_week
#         self.order_in_schedule = order_in_schedule
#         self.patients = patients

#     # Getters and setters 

#     def get_order_in_week(self):
#         return self._order_in_week
    
#     def set_order_in_week(self, new:int):
#         self._order_in_week = new
    
#     order_in_week = property(get_order_in_week, set_order_in_week)


#     def get_order_in_schedule(self):
#         return self._order_in_schedule
    
#     def set_order_in_schedule(self, new:int):
#         self._order_in_schedule = new
    
#     order_in_schedule = property(get_order_in_schedule, set_order_in_schedule)


#     def get_patients(self):
#         return self._patients
    
#     def set_patients(self, new:list[Patient]):
#         self._patients = new
    
#     patients = property(get_patients, set_patients)

#     # Methods

#     def proportion_urgency(self):
#         pass

#     def metric_undertime(self):
#         pass

