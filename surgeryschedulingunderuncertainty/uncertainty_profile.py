# Python STL
from abc import ABC, abstractmethod
import random

# Packages
import numpy as np
import scipy.stats as ss

# Module's classes
#


class UncertaintyProfile(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def sample(self, size):
        pass



class LogNormalDistribution(UncertaintyProfile):

    def __init__(self, param_s, param_scale):
        self.param_s = param_s
        self.param_scale = param_scale

    # Getters and setters
        
    def get_param_s(self):
        return self._param_s
    
    def set_param_s(self, new:float):
        self._param_s = new
    
    param_s = property(get_param_s, set_param_s)


    def get_param_scale(self):
        return self._param_scale
    
    def set_param_scale(self, new:float):
        self._param_scale = new
    
    param_scale = property(get_param_scale, set_param_scale)


    # Abstract methods implementation

    def sample(self, size):
        """
        This method sample from the lognormal distribution.
        Pay attenction: we have to handle a diversity between parameters provided 
        by ngboos and scipy sampler. The following transformations are studied to 
        match the two convenctions.
        :param size: number or sampled value
        :return: np vector containg samples
        """

        # Rename just to make the term convenction clearer
        mean = self.param_scale
        std = self.param_s

        # Transform the parameters
        my_mu = np.log(mean**2/np.sqrt(mean**2 + std**2))
        my_sigma = np.log(1+(std**2)/(mean**2))

        # Sampling from normal 
        samples = ss.norm.rvs(loc = my_mu, scale = my_sigma, size = size)

        # Trasform the samples
        samples = np.exp(samples)

        return samples




class NormalDistribution(UncertaintyProfile):

    def __init__(self, param_loc, param_scale):
        self.param_loc = param_loc
        self.param_scale = param_scale


    # Getters and setters
        
    def get_param_loc(self):
        return self._param_loc
    
    def set_param_loc(self, new:float):
        self._param_loc = new
    
    param_loc = property(get_param_loc, set_param_loc)


    def get_param_scale(self):
        return self._param_scale
    
    def set_param_scale(self, new:float):
        self._param_scale = new
    
    param_scale = property(get_param_scale, set_param_scale)


    # Abstract methods implementation

    def sample(self, size):
        return ss.norm.rvs(loc = self.param_loc, scale = self.param_scale, size = size)




class HistogramModel(UncertaintyProfile):

    def __init__(self, values: list[float], probs: list[float]):

        # Check that values and probs are of the same lenght
        if not len(values) == len(probs):
            raise ValueError("The values vector and the probs vector have a different number of components.")

        # Check that the sum of probabilities is approximately one
        total_prob = np.sum(probs)
        tollerance = 1e-6
        if not np.isclose(total_prob, 1.0, atol=tollerance):
            raise ValueError(f"The sum of probabilities is not one (tolerance={tollerance}).")
        
        # Ordering
        sorting_index = np.argsort(values)

        values = values[sorting_index]
        probs  = probs[sorting_index]

        # Assigning
        self.values = values
        self.probs = probs

    # Getters and setters
    def get_values(self):
        return self._values
    
    def set_values(self, new:list[float]):

        # Check that values and probs are of the same lenght
        if not len(new) == len(self.probs):
            raise ValueError("The values vector has not the same length of the probs, use set_values_and_probs to change both.")

        self._values = new
    
    values = property(get_values, set_values)


    def get_probs(self):
        return self._probs
    
    def set_probs(self, new:list[float]):

        # Check that values and probs are of the same lenght
        if not len(new) == len(self.values):
            raise ValueError("The probs vector has not the same length of the values, use set_values_and_probs to change both.")

        # Check that the sum of probabilities is approximately one
        total_prob = np.sum(new)
        tollerance = 1e-6
        if not np.isclose(total_prob, 1.0, atol=tollerance):
            raise ValueError(f"The sum of probabilities is not one (tolerance={tollerance}).")

        # Set new value
        self._probs = new
    
    probs = property(get_probs, set_probs)

    def set_values_and_probs(self, values:list[float], probs:list[float]):
        
        # Check that values and probs are of the same lenght
        if not len(values) == len(probs):
            raise ValueError("The values vector and the probs vector have a different number of components.")

        # Check that the sum of probabilities is approximately one
        total_prob = np.sum(probs)
        tollerance = 1e-6
        if not np.isclose(total_prob, 1.0, atol=tollerance):
            raise ValueError(f"The sum of probabilities is not one (tolerance={tollerance}).")
        
        self.values = values
        self.probs = probs


    # Abstract methods implementation
    def sample(self, size):
        self.bin_sampling(size)
        #return np.random.choice(self.values, size=size, p=self.probs)
    
    # Specific methods
    def pointwise_sampling(self, size):
        np.random.choice(self.values, size=size, p=self.probs)

    def bin_sampling(self, size):
        
        # Getting means between values
        bins_extrema = (self.values[:-1] + self.values[1:]) / 2

        # Compute weighted moments
        weighted_mean = np.sum(self.values * self.probs)
        weighted_variance = np.sum((self.values - weighted_mean)**2 * self.probs)
        weighted_skewness = np.sum((self.values - weighted_mean)**3 * self.probs) / np.power(np.sqrt(weighted_variance), 3)

        dist = ss.pearson3(weighted_skewness, loc=weighted_mean, scale=np.sqrt(weighted_variance))

        bins_extrema = np.concatenate(([dist.ppf(self.probs[0]/4)], bins_extrema, [dist.ppf(1-self.probs[0]/4)]))

        selected_bin = np.random.choice(len(self.probs), p=self.probs)

        start = bins_extrema[selected_bin]
        end = bins_extrema[selected_bin+1]

        dist = ss.uniform(loc=start, scale=end-start)
        
        return dist.rvs(size=size)

    def continuous_sampling(self, size):

        # Compute weighted moments
        weighted_mean = np.sum(self.values * self.probs)
        weighted_variance = np.sum((self.values - weighted_mean)**2 * self.probs)
        weighted_skewness = np.sum((self.values - weighted_mean)**3 * self.probs) / np.power(np.sqrt(weighted_variance), 3)

        dist = ss.pearson3(weighted_skewness, loc=weighted_mean, scale=np.sqrt(weighted_variance))

        return dist.rvs(size=size)



class BalancedHistogramModel(UncertaintyProfile):

    def __init__(self, values: list[float]):
        
        self.profile = HistogramModel(values=values, probs=np.tile(1/len(values), len(values)))

        self.values = values
        self.prob = 1 / len(values)

    # Getters and setters
    def get_values(self):
        return self.profile.get_values
    
    def set_values(self, new:list[float]):
        self.profile.set_values_and_probs(values = new, 
                                          probs = np.tile(1/len(new), len(new)))
    
    values = property(get_values, set_values)

    # Abstract methods implementation
    def sample(self, size):
        return self.sample(size)

    # Specific methods
    def pointwise_sampling(self, size):
        self.profile.pointwise_sampling(size)

    def bin_sampling(self, size):
        self.profile.bin_sampling(size)

    def continuous_sampling(self, size):
        self.profile.continuous_sampling(size)

