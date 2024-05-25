

import numpy as np

import math


def equiprobability_allocation_from_sampling(samples_ordered, robusttime):
    # todo docstring
    sample_dimension = np.shape(samples_ordered)[1]

    for index in range(math.ceil(sample_dimension / 2), sample_dimension):
        sum_of_times = 0
        for sample in samples_ordered:
            sum_of_times += sample[index]
        if sum_of_times >= robusttime:
            return index

    raise ValueError("Total time does not get larger than the overtime")
