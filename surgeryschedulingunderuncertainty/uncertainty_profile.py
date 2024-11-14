# Python STL
from abc import ABC, abstractmethod
import random

# Packages
import numpy as np
import scipy.stats as ss

# Modules


class UncertaintyProfile(ABC):

    def __init__(self, nominal_value : float):
        self._nominal_value = nominal_value
        pass

    # Getters and setters
    def get_nominal_value(self):
        return self._nominal_value
    def set_nominal_value(self, new:float):
        self._nominal_value = new
    nominal_value = property(get_nominal_value, set_nominal_value)

    # Abstract methods
    @abstractmethod
    def uncertainty_summary(self):
        pass
    
    @abstractmethod
    def sample(self, size):
        pass
    
    @abstractmethod
    def percent_point_function(self):
        pass
    
    



class LogNormalDistribution(UncertaintyProfile):

    def __init__(self, param_s, param_scale):
            
        super().__init__(nominal_value = param_scale**2/np.sqrt(param_scale**2 + param_s**2))

        
        self._param_s = param_s
        self._param_scale = param_scale

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
    
    def uncertainty_summary(self):
        
        return "shape: {}, scale: {}".format(self._param_scale, self._param_s)

        
        

    def sample(self, size):
        """
        This method sample from the lognormal distribution.
        Pay attenction: we have to handle a diversity between parameters provided 
        by ngboos and scipy sampler. The following transformations are studied to 
        match the two convenctions.
        :param size: number or sampled value
        :return: np vector containg samples
        """
        
        # mean = self._param_scale
        # std = self._param_s

        # my_mu = np.log(mean**2/np.sqrt(mean**2 + std**2))
        # my_sigma = np.log(1+(std**2)/(mean**2))

        # return np.exp(ss.norm.rvs(loc = my_mu, scale = my_sigma, size = size))
        
        

        # Rename just to make the term convenction clearer
        mean = self._param_scale
        std = self._param_s

        # # Transform the parameters
        # my_mu = np.log(mean**2/np.sqrt(mean**2 + std**2))
        # my_sigma = np.log(1+(std**2)/(mean**2))

        # # Sampling from normal 
        # samples = ss.norm.rvs(loc = my_mu, scale = my_sigma, size = size)

        # # Trasform the samples
        # samples = np.exp(samples)

        # #return samples
    
        return ss.lognorm.rvs(std, loc=0, scale=mean, size=size, random_state=None)

    def percent_point_function(self, probability):
        """
        Using this method for the chance constraints implementor

        """
        # SHIT
        #return ss.lognorm.ppf(probability, s= , loc= , scale = )
        
        # Rename just to make the term convenction clearer
        mean = self._param_scale
        std = self._param_s

        # # Transform the parameters
        # my_mu = np.log(mean**2/np.sqrt(mean**2 + std**2))
        # my_sigma = np.log(1+(std**2)/(mean**2))

        # # Get the percent point from normal 
        # value = ss.norm.ppf(q = probability, loc = my_mu, scale = my_sigma)

        # # Trasform the percent point
        # value = np.exp(value)

        # return value
        
        return ss.lognorm.ppf(q = probability, s= std, loc=0, scale=mean)
    

        
        


class NormalDistribution(UncertaintyProfile):

    def __init__(self, param_loc, param_scale):
        
        super().__init__(nominal_value = param_loc)

        
        self._param_loc = param_loc
        self._param_scale = param_scale


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
        return ss.norm.rvs(loc = self._param_loc, scale = self._param_scale, size = size)




class HistogramModel(UncertaintyProfile):

    def __init__(self, values: list[float], probs: list[float]):
        
        
        #super().__init__(nominal_value = param_loc) # TODO!

        
        values = np.array(values)
        probs = np.array(probs)

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
        self._values = values
        self._probs = probs

    # Getters and setters
    def get_values(self):
        return self._values
    
    def set_values(self, new:list[float]):
        new = np.array(new)

        # Check that values and probs are of the same lenght
        if not len(new) == len(self._probs):
            raise ValueError("The values vector has not the same length of the probs, use set_values_and_probs to change both.")

        self._values = new
    
    values = property(get_values, set_values)


    def get_probs(self):
        return self._probs
    
    def set_probs(self, new:list[float]):
        new = np.array(new)

        # Check that values and probs are of the same lenght
        if not len(new) == len(self._values):
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
        values = np.array(values)
        probs = np.array(probs)
        
        # Check that values and probs are of the same lenght
        if not len(values) == len(probs):
            raise ValueError("The values vector and the probs vector have a different number of components.")

        # Check that the sum of probabilities is approximately one
        total_prob = np.sum(probs)
        tollerance = 1e-6
        if not np.isclose(total_prob, 1.0, atol=tollerance):
            raise ValueError(f"The sum of probabilities is not one (tolerance={tollerance}).")
        
        self._values = values
        self._probs = probs


    # Abstract methods implementation
    def sample(self, size):
        return self.bin_sampling(size)


    # Specific methods
    def pointwise_sampling(self, size):
        return np.random.choice(self._values, size=size, p=self._probs)

    def bin_sampling(self, size):
        # Getting means between values
        bins_extrema = (self._values[:-1] + self._values[1:]) / 2

        # Compute weighted moments
        weighted_mean = np.sum(self._values * self._probs)
        weighted_variance = np.sum((self._values - weighted_mean)**2 * self._probs)
        weighted_skewness = np.sum((self._values - weighted_mean)**3 * self._probs) / np.power(np.sqrt(weighted_variance), 3)

        dist = ss.pearson3(weighted_skewness, loc=weighted_mean, scale=np.sqrt(weighted_variance))

        bins_extrema = np.concatenate(([dist.ppf(self._probs[0]/4)], bins_extrema, [dist.ppf(1-self._probs[0]/4)]))

        selected_bin = np.random.choice(len(self._probs), p=self._probs)

        start = bins_extrema[selected_bin]
        end = bins_extrema[selected_bin+1]

        dist = ss.uniform(loc=start, scale=end-start)
        
        return dist.rvs(size=size)

    def continuous_sampling(self, size):
        # Compute weighted moments
        weighted_mean = np.sum(self._values * self._probs)
        weighted_variance = np.sum((self._values - weighted_mean)**2 * self._probs)
        weighted_skewness = np.sum((self._values - weighted_mean)**3 * self._probs) / np.power(np.sqrt(weighted_variance), 3)

        dist = ss.pearson3(weighted_skewness, loc=weighted_mean, scale=np.sqrt(weighted_variance))

        return dist.rvs(size=size)



class BalancedHistogramModel(UncertaintyProfile):

    def __init__(self, values: list[float]):        
        self._profile = HistogramModel(values=values, probs=np.tile(1/len(values), len(values)))

    # Getters and setters
    def get_values(self):
        return self._profile.get_values()
    
    def set_values(self, new:list[float]):
        self._profile.set_values_and_probs(values = new, 
                                          probs = np.tile(1/len(new), len(new)))
    
    values = property(get_values, set_values)

    def get_probs(self):
        return self._profile.get_probs()
    
    def set_probs(self, new:list[float]):
        self._profile.set_probs(new)

    probs = property(get_probs, set_probs)

    
    # Abstract methods implementation
    def sample(self, size):
        return self._profile.sample(size)

    # Specific methods
    def pointwise_sampling(self, size):
        return self._profile.pointwise_sampling(size)

    def bin_sampling(self, size):
        return self._profile.bin_sampling(size)

    def continuous_sampling(self, size):
        return self._profile.continuous_sampling(size)

