# Python STL
from abc import ABC, abstractmethod

# Packages

# Modules
from .patient import Patient

class Block(ABC):
    
    def __init__(self, duration: int, equipes: list[str], room: str, weekday: int, order_in_day: int):
        self._duration = duration
        self._equipes = equipes
        self._weekday = weekday
        self._room = room 
        self._order_in_day = order_in_day

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
    
    def get_room(self):
        return self._room
    
    def set_room(self, new: str):
        self._room = new
    
    room = property(get_room, set_room)
    
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

    def __init__(self, duration: int, equipes: list[str], room: str, weekday: int, order_in_day: int, order_in_master: int):
        super().__init__(duration=duration, equipes=equipes, room=room, weekday=weekday, order_in_day=order_in_day)
        self._order_in_master = order_in_master

    def __str__(self):
        return f"""Master Block number {self._order_in_master}
                \nEquipe: {self._equipes}
                \nDuration: {self._duration}
                \nRoom: {self._room}
                \nWeekday: {self._weekday}
                \nNumber in day: {self._order_in_day}
                """

    # Getters and setters
    def get_order_in_master(self):
        return self._order_in_master
    
    def set_order_in_master(self, new:int):
        self._order_in_master = new
    
    order_in_master = property(get_order_in_master, set_order_in_master)



class ScheduleBlock(Block):

    def __init__(self, duration: int, equipes: list[str], room: str, weekday: int, order_in_day: int, 
                 order_in_week: int, order_in_schedule: int, patients: list[Patient] = None):
        
        super().__init__(duration, equipes, room, weekday, order_in_day)
        
        self._order_in_week = order_in_week
        self._order_in_schedule = order_in_schedule
        
        # if patients argument is None we create an empty list to store the patients. Use add_patient to populate the list.
        if patients: 
            self._patients = patients
        else:
            self._patients = []

    # Getters and setters 

    def get_order_in_week(self):
        return self._order_in_week
    def set_order_in_week(self, new:int):
        self._order_in_week = new
    order_in_week = property(get_order_in_week, set_order_in_week)

    def get_order_in_schedule(self):
        return self._order_in_schedule    
    def set_order_in_schedule(self, new:int):
        self._order_in_schedule = new
    order_in_schedule = property(get_order_in_schedule, set_order_in_schedule)

    def get_patients(self):
        return self._patients    
    def set_patients(self, new:list[Patient]):
        self._patients = new
    patients = property(get_patients, set_patients)

    # Methods
    
    def add_patient(self, new:Patient):
        self._patients.append(new)
        return True
    

    def proportion_urgency(self):
        pass

    def metric_undertime(self):
        pass

