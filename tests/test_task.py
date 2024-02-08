# Python STL
import unittest
from unittest.mock import patch

# Packages
from hypothesis import given, strategies as st
import numpy as np

# Modules
from surgeryschedulingunderuncertainty.patient import Patient

# Objects of test
from surgeryschedulingunderuncertainty.task import Task



# TODO: va testato anche master scheduling



class TestTask(unittest.TestCase):
    
    def test_task_arguments(self):
        """ If instantiatd without argument, raise error. """
        with self.assertRaises(TypeError):
            Task()
    
    def setUp(self):
        self.task1 = Task(
            name="Test task 1",
            num_of_weeks= 2,
            num_of_patients= 4,
            robustness_risk= 0.2,
            robustness_overtime= 10,
            urgency_to_max_waiting_time={0:60, 1:30, 2:15}
            )
        
        self.task2 = Task(
            name="Test task 2",
            num_of_weeks= 5,
            num_of_patients= 2,
            robustness_risk= 0.4,
            robustness_overtime= 60,
            urgency_to_max_waiting_time={0:10, 1:30, 2:15, 3:22, 4:19}
            )
        
        self.task3 = Task(
            name="Test task 3",
            num_of_weeks= 9,
            num_of_patients= 3,
            robustness_risk= 0.8,
            robustness_overtime= 30,
            urgency_to_max_waiting_time={0:12, 1:30, 2:15, 3:61}
            )
        
        self.patient1 = Patient(id = 1,
                           equipe = 'A',
                           urgency = 2)
        
        self.patient2 = Patient(id = 2,
                           equipe = 'A',
                           urgency = 2)

        self.patient3 = Patient(id = 3,
                           equipe = 'A',
                           urgency = 2)
        
        self.patient4 = Patient(id = 4,
                           equipe = 'A',
                           urgency = 2)

        
    def test_members(self):
        """ Testing the values assigned to members. """
        self.assertEqual(self.task1.name, "Test task 1")
        self.assertEqual(self.task2.name, "Test task 2")

        self.assertEqual(self.task2.num_of_weeks, 5)
        self.assertEqual(self.task3.num_of_weeks, 9)

        self.assertEqual(self.task1.num_of_patients, 4)
        self.assertEqual(self.task3.num_of_patients, 3)

        self.assertEqual(self.task1.robustness_risk, .2)
        self.assertEqual(self.task2.robustness_risk, .4)

        self.assertEqual(self.task2.robustness_overtime, 60)
        self.assertEqual(self.task3.robustness_overtime, 30)

    
    def test_patients_length(self):
        """ Testing that the control on the length of patient list works fine. """
        
        list_of_patients1 = [self.patient1, self.patient2, self.patient3, self.patient4]
        list_of_patients1_bad = [self.patient1, self.patient2, self.patient3]

        list_of_patients2 = [self.patient1,  self.patient4]
        list_of_patients2_bad = [self.patient1, self.patient2, self.patient3]

        list_of_patients3 = [self.patient2, self.patient3, self.patient4]
        list_of_patients3_bad = [self.patient1, self.patient3]

        try:
            self.task1.patients = list_of_patients1
        except ValueError:
            self.fail("The error is risen even if the lengths match.")

        with self.assertRaises(ValueError):
            self.task1.patients = list_of_patients1_bad

        try:
            self.task2.patients = list_of_patients2
        except ValueError:
            self.fail("The error is risen even if the lengths match.")

        with self.assertRaises(ValueError):
            self.task2.patients = list_of_patients2_bad

        try:
            self.task3.patients = list_of_patients3
        except ValueError:
            self.fail("The error is risen even if the lengths match.")

        with self.assertRaises(ValueError):
            self.task3.patients = list_of_patients3_bad

    

    def test_patients_ids(self):
        """ Testing that the control on the duplicates ids in the patient list works fine. """
        list_of_patients = [self.patient1, self.patient2, self.patient3, self.patient3]

        with self.assertRaises(ValueError):
            self.task1.patients = list_of_patients

    
    
    def test_urgency_to_urgency_grade(self):
        """ Testing the deduction of urgency to urgency grades mapping. """
        self.assertEqual(self.task1.urgency_to_urgency_grades, {0:15, 1:30, 2:60})
        self.assertEqual(self.task2.urgency_to_urgency_grades, {0:19, 1:22, 2:15, 3:30, 4:10})
        self.assertEqual(self.task3.urgency_to_urgency_grades, {0:61, 1:15, 2:30, 3:12})




if __name__ == '__main__':
    unittest.main()