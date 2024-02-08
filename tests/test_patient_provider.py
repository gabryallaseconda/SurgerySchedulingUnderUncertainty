# Python STL
import unittest
from unittest.mock import patch

# Packages
from hypothesis import given, strategies as st
import numpy as np

# Modules
from surgeryschedulingunderuncertainty.patient import Patient
from surgeryschedulingunderuncertainty.task import Task

# Objects of test
from surgeryschedulingunderuncertainty.patients_provider import (
    Patient,
    PatientsFromHistoricalDataProvider
)



class TestPatientsFromHistoricalDataProvider(unittest.TestCase):
    
    def test_log_normal_distribution_arguments(self):
        with self.assertRaises(TypeError):
            PatientsFromHistoricalDataProvider()

    def setUp(self):
        self.uncertaintyprofile = LogNormalDistribution(param_s=1, param_scale=1)

    @patch('scipy.stats.norm.rvs')
    def test_log_normal_distribution_sample_mock(self, mock_obj):
        mock_obj.return_value = np.array([2,3])
        result = np.array([np.exp(2), np.exp(3)])
        self.assertTrue(np.all(self.uncertaintyprofile.sample(size = 3) == result)) 

    @given(st.floats(2, 400), st.floats(2, 400))
    def test_log_normal_distribution_sample_property(self, param_s, param_scale):

        size = 10000
        tollerance = 1

        uncertaintyprofile = LogNormalDistribution(param_s, param_scale)
        samples = np.log(uncertaintyprofile.sample(size))

        new_mean = np.log(param_scale**2/np.sqrt(param_scale**2 + param_s**2))
        new_std = np.log(1+(param_s**2)/(param_scale**2))

        self.assertTrue(np.isclose(np.mean(samples), new_mean, atol=tollerance))
        self.assertTrue(np.isclose(np.std(samples), new_std, atol=tollerance))




class TestNormalDistribution(unittest.TestCase):
    
    def test_normal_distribution_arguments(self):
        with self.assertRaises(TypeError):
            NormalDistribution()

    def setUp(self):
        self.uncertaintyprofile = NormalDistribution(param_loc=1, param_scale=1)

    @patch('scipy.stats.norm.rvs')
    def test_normal_distribution_sample_mock(self, mock_obj):
        mock_obj.return_value = np.array([4,5,6])
        result = np.array([4,5,6])
        self.assertTrue(np.all(self.uncertaintyprofile.sample(size = 3) == result)) 

    @given(st.floats(.1, 400), st.floats(.1, 400))
    def test_normal_distribution_sample_property(self, param_loc, param_scale):

        size = 10000
        tollerance = 3

        # problemi di stabilità numerica
        if (param_scale > 10) & (param_scale > param_loc):
            tollerance = (param_scale/param_loc) * np.log(param_scale)
        # ancora problemi di stabilità numerica
        if (param_loc > 100) & (param_scale > 100):
            tollerance = np.mean([param_loc, param_scale])/5

        uncertaintyprofile = NormalDistribution(param_loc, param_scale)
        samples = uncertaintyprofile.sample(size)

        self.assertTrue(np.isclose(np.mean(samples), param_loc, atol=tollerance))
        self.assertTrue(np.isclose(np.std(samples), param_scale, atol=tollerance))


# class TestHistogramModel(unittest.TestCase):
    
#     def test_histogram_model_arguments(self):
#         with self.assertRaises(TypeError):
#             HistogramModel()

#     def setUp(self):
#         self.uncertaintyprofile = HistogramModel([4.7, 5.2, 9.1, 12.3])

#     @patch('random.choice')
#     def test_histogram_model_sample_mock(self, mock_obj):
#         mock_obj.return_value = np.array([2,3])
#         result = np.array([2, 3])
#         self.assertTrue(np.all(self.uncertaintyprofile.sample(size = 3) == result)) 

#     @given(st.lists(st.floats))  #### CONTINUARE DA QUI!!!!
#     def test_histogram_model_sample_property(self, values):

#         size = 10000
#         tollerance = 1

#         uncertaintyprofile = HistogramDistribution(param_s, param_scale)
#         samples = np.log(uncertaintyprofile.sample(size))

#         new_mean = np.log(param_scale**2/np.sqrt(param_scale**2 + param_s**2))
#         new_std = np.log(1+(param_s**2)/(param_scale**2))

#         self.assertTrue(np.isclose(np.mean(samples), new_mean, atol=tollerance))
#         self.assertTrue(np.isclose(np.std(samples), new_std, atol=tollerance))






if __name__ == '__main__':
    unittest.main()